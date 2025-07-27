#!/usr/bin/env python3
"""
Utility that materialises an evaluation suite for a generated MCP server.

Called from MCPGenerator when --generate-eval is supplied.
"""

import os
import json
import uuid
import asyncio
import re
import httpx, os
from typing import Dict, List, Any
import yaml
from cnoe_agent_utils import LLMFactory
from langchain_core.messages import SystemMessage
def _build_arg_spec(path: str, method: str, spec: Dict[str, Any]) -> str:
    """Return a JSON-like string describing the callable’s arguments."""
    op = spec["paths"][path][method]
    args: Dict[str, str] = {}

    # path & query parameters
    for p in op.get("parameters", []):
        if "$ref" in p:                                           # resolve refs
            ref_path = p["$ref"]
            resolved = spec
            for part in ref_path.lstrip("#/").split("/"):
                resolved = resolved[part]
            p = resolved
        if p.get("in") in {"path", "query"}:
            args[p["name"]] = p.get("schema", {}).get("type", "string")

    # JSON body
    if "requestBody" in op:
        sch = op["requestBody"]["content"].get("application/json", {}).get("schema", {})
        if "$ref" in sch:
            ref_path = sch["$ref"]
            resolved = spec
            for part in ref_path.lstrip("#/").split("/"):
                resolved = resolved[part]
            sch = resolved
        if sch.get("type") == "object":
            for n, pr in sch.get("properties", {}).items():
                args[n] = pr.get("type", "string")
    return json.dumps(args, ensure_ascii=False)

def _camel_to_snake(name: str) -> str:
    out = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    out = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", out)
    return out.replace("-", "_").lower()


async def _tool_output_async(
    llm,
    prompt: str,
    tool_name: str,
    arg_spec: str,
    tool_desc: str,
    path: str,
    method: str,
) -> tuple[str, str, str]:
    """
    Given the *user prompt*, produce:
      • JSON string with function arguments,
      • JSON string with a plausible tool response,
      • assistant answer text.
    Returns (args_json, tool_output_json, answer_text).
    """
    mock_api_flag = os.getenv("MOCK_API", "1").lower() not in {"0", "false", ""}

    # ---- build system prompt -------------------------------------------------
    _lines = [
        "You simulate both the caller and backend of a Komodor API, a Kubernetes management platform.",
        f"Tool/function: {tool_name}",
        f"Tool description: {tool_desc}",
        f"Argument schema: {arg_spec}",
        "",
        "For the **USER REQUEST** below:",
        "  1) craft concrete JSON arguments matching the schema;",
    ]
    if mock_api_flag:
        _lines.append("  2) invent a realistic JSON response from the backend;")
        _lines.append("  3) write the assistant's natural-language reply.")
    else:
        _lines.append("  2) write the assistant's natural-language reply.")
    _lines.extend(
        [
            "",
            'Return ONLY a JSON object with keys:',
            '  "args":        <JSON object>,',
        ]
        + (['  "tool_output": <JSON object>,'] if mock_api_flag else [])
        + ['  "answer":      <string>', "No markdown, no code-fences."],
    )
    sys_msg_base = SystemMessage(content="\n".join(_lines))

    max_attempts = 3
    last_err: str | None = None

    for attempt in range(max_attempts):
        msgs = [sys_msg_base]
        if last_err:
            msgs.append(
                SystemMessage(
                    content=(
                        "The previous attempt failed with the following error:\n"
                        f"{last_err}\n"
                        "Please correct the arguments and try again. "
                        "Return ONLY the corrected JSON object."
                    )
                )
            )
        msgs.append(SystemMessage(prompt))

        resp = await llm.ainvoke(msgs)

        try:
            data = json.loads(resp.content)
            args_json = json.dumps(data.get("args", {}), ensure_ascii=False)
            answer = data.get("answer", "").strip()
        except Exception as e:
            last_err = f"Invalid JSON returned by LLM: {e}"
            continue  # retry

        # ------------------------------------------------------------- backend
        if mock_api_flag:
            tool_output_json = json.dumps(data.get("tool_output", {}), ensure_ascii=False)
            return args_json, tool_output_json, answer

        try:  # real API call
            base_url = os.getenv("KOMODOR_API_URL") or os.getenv("{{ mcp_name | upper }}_API_URL")
            token    = os.getenv("KOMODOR_TOKEN")   or os.getenv("{{ mcp_name | upper }}_TOKEN")
            if not base_url or not token:
                raise ValueError("KOMODOR_API_URL / KOMODOR_TOKEN env vars are required when MOCK_API=0")

            args_dict = json.loads(args_json) if isinstance(args_json, str) else args_json
            # substitute path parameters  {param}
            url = base_url + path
            for k, v in args_dict.items():
                url = url.replace(f"{{{k}}}", str(v)).replace(f"{{path_{k}}}", str(v))

            headers = {"X-API-KEY": f"{token}"}
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.request(method.upper(), url, json=args_dict, params=args_dict, headers=headers)
                # Retry if the backend did not return success
                if not 200 <= response.status_code < 300:
                    last_err = (
                        f"Non-2xx status code {response.status_code}: "
                        f"{response.text[:500]}"  # trim long bodies
                    )
                    continue  # ask the LLM to resubmit corrected arguments
                try:
                    tool_output_json = json.dumps(response.json(), ensure_ascii=False)
                except Exception:
                    tool_output_json = json.dumps({"status_code": response.status_code, "text": response.text}, ensure_ascii=False)
                return args_json, tool_output_json, answer
        except Exception as e:
            last_err = str(e)
            continue  # retry

    # Fallback after all retries failed
    return "{}", "{}", f"[LLM failed after {max_attempts} attempts] {last_err or ''}"

def _generate_tool_outputs_bulk(
    prompts:    List[str],
    tool_names: List[str],
    arg_specs:  List[str],
    tool_descs: List[str],
    paths:      List[str],
    methods:    List[str],
    agent_dir:  str,                         # NEW
    mcp_name:   str,                         # NEW
) -> List[tuple[str, str, str]]:
    import sys
    sys.path.insert(0, agent_dir)       # make agent.py importable
    from agent import create_agent      # local generated agent
    import importlib, pkgutil, inspect

    pkg_name = f"mcp_{mcp_name}"
    tools_pkg = importlib.import_module(f"{pkg_name}.tools")

    # Build mapping: tool-function name -> function object
    tool_func_map: dict[str, Any] = {}
    for _, modname, _ in pkgutil.walk_packages(tools_pkg.__path__):
        mod = importlib.import_module(f"{pkg_name}.tools.{modname}")
        for name, obj in inspect.getmembers(mod):
            if inspect.iscoroutinefunction(obj) or callable(obj):
                tool_func_map[name] = obj

    import re  # already imported at top; keep if present

    def _lookup_tool(name: str):
        """Return the generated function matching *name*.

        Falls back to the generator’s naming convention that replaces
        “/ . -” by “_”.
        """
        if name in tool_func_map:
            return tool_func_map[name]
        alt = re.sub(r"[./-]", "_", name)
        if alt in tool_func_map:
            return tool_func_map[alt]
        raise KeyError(
            f"Tool function {name!r} not found (tried {alt!r}). "
            f"Available: {sorted(tool_func_map)[:20]}..."
        )

    from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
    import uuid

    async def _agent_runner():
        """Run all prompt/tool pairs in parallel and preserve order."""
        from langchain_core.messages import AIMessage, ToolMessage

        async def _process(prompt: str, tool: str) -> tuple[str, str, str]:
            agent = await create_agent(tools=[_lookup_tool(tool)])
            cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
            messages = [
                SystemMessage(
                    content=(
                        "If the API fails with error 400 try to fix the errors and retry up to "
                        "two more times. Do not ask the user for input."
                    )
                ),
                ("user", prompt),
            ]
            res = await agent.ainvoke({"messages": messages}, cfg)
            msgs = res["messages"]

            args_json, tool_output_json, answer = "{}", "{}", ""
            for m in msgs:
                if isinstance(m, AIMessage) and m.tool_calls:
                    tc = m.tool_calls[0]
                    call_args_raw = (
                        tc.get("function", {}).get("arguments", {})
                        if isinstance(tc, dict)
                        else getattr(tc, "function", {}).get("arguments", {})
                    )
                    if isinstance(call_args_raw, str):
                        try:
                            call_args_raw = json.loads(call_args_raw)
                        except Exception:
                            call_args_raw = {"raw": call_args_raw}
                    args_json = json.dumps(call_args_raw, ensure_ascii=False)
                elif isinstance(m, ToolMessage):
                    tool_output_json = (
                        json.dumps(m.content, ensure_ascii=False)
                        if not isinstance(m.content, str)
                        else m.content
                    )
            for m in reversed(msgs):
                if isinstance(m, AIMessage) and not m.tool_calls:
                    answer = m.content
                    break
            return args_json, tool_output_json, answer

        tasks = [
            _process(p, t) for p, t in zip(prompts, tool_names)
        ]
        return await asyncio.gather(*tasks)

    return asyncio.run(_agent_runner())




def _mk_trajectory(
    user_prompt: str,
    tool_name: str,
    args_json: str,
    tool_output: str,
    answer: str,
    agent_name: str,        # NEW
) -> List[Dict[str, Any]]:
    call_id = uuid.uuid4().hex
    return [
        {"role": "user", "agent": "__start__", "content": user_prompt},
        {
            "role": "assistant",
            "agent": agent_name,           # use MCP name
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "id": call_id,
                    "function": {
                        "name": tool_name,
                        "arguments": (
                            json.loads(args_json) if isinstance(args_json, str) else args_json
                        ),
                    },
                }
            ],
        },
        {
            "role": "tool",
            "agent": "mcp_tools",
            # Parse JSON so the dataset YAML contains structured output
            "content": (
                json.loads(tool_output)
                if isinstance(tool_output, str)
                else tool_output
            ),
            "tool_call_id": call_id,
        },
        {"role": "assistant", "agent": agent_name, "content": answer},
    ]

async def _llm_variations_async(
    llm,
    seed: str,
    n: int,
    tool_name: str,
    arg_spec: str,
    tool_desc: str,
) -> List[str]:
    """
    Async helper that asks the LLM for *n* paraphrases of *seed*.
    Falls back to deterministic stubs if LLM is unavailable.
    """
    if not hasattr(llm, "ainvoke"):  # stub or sync-only LLM
        return [f"{seed} (variant {i+1})" for i in range(n)]

    prompt = (
        "You are a helpful assistant tasked with creating user requests for a Komodor API, a Kubernetes management platform.\n"
        f"The API function to be invoked is `{tool_name}` "
        f"(description: {tool_desc}). "
        f"It must be called with JSON arguments that match this schema: {arg_spec}.\n\n"
        f"Generate {n} different, natural-language instructions that would lead the assistant "
        "to call this function with sensible concrete argument values (e.g., realistic names, "
        "ids, quantities, etc.).\n"
        "Return ONLY a JSON list containing the prompts (no markdown, no code-fences)."
    )
    resp = await llm.ainvoke([SystemMessage(prompt)])
    try:
        return json.loads(resp.content)
    except Exception:
        return [line.strip("- ") for line in resp.content.split("\n") if line.strip()][:n]


def _generate_variations_bulk(
    seeds: List[str],
    n: int,
    tool_names: List[str],
    arg_specs: List[str],
    tool_descs: List[str],
) -> List[List[str]]:
    """
    Create paraphrases for *seeds* concurrently using a single event loop.
    Returns a list parallel to *seeds* where each element is the list of n variants.
    """
    llm = LLMFactory().get_llm()

    async def _runner():
        results = await asyncio.gather(
            *[
                _llm_variations_async(llm, seed, n, tool, arg, desc)
                for seed, tool, arg, desc in zip(seeds, tool_names, arg_specs, tool_descs)
            ],
            return_exceptions=True,            # ← collect errors
        )
        for res in results:                   # bubble up first failure
            if isinstance(res, Exception):
                raise res
        return results

    return asyncio.run(_runner())


def generate_eval_suite(
    *,
    spec: Dict[str, Any],
    mcp_name: str,
    tools_map: Dict[str, List[str]],
    dest_dir: str,
    num_prompts: int = 5,
) -> None:
    """
    Build everything under *dest_dir* required to run the pytest-based
    evaluation shown in examples/eval_codegen/example/.
    """
    # 1. produce synthetic prompt / reference data --------------------------------

    seeds: List[str] = []
    tool_names_for_seeds: List[str] = []
    arg_specs_for_seeds: List[str] = []
    tool_descs_for_seeds: List[str] = []
    meta:  List[tuple[str, str, str]] = []   # (path, method, summary) for later alignment
    for path, ops in spec.get("paths", {}).items():
        for method, op in ops.items():
            summary = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
            seed_prompt = f"{summary}"
            seeds.append(seed_prompt)

            tool_name = _camel_to_snake(
                op.get("operationId") or f"{method}_{path.strip('/')}"
            )
            tool_names_for_seeds.append(tool_name)

            arg_specs_for_seeds.append(_build_arg_spec(path, method, spec))

            op_desc = op.get("description", "") or summary
            tool_descs_for_seeds.append(op_desc)

            meta.append((path, method, summary))

    all_variants = _generate_variations_bulk(
        seeds,
        num_prompts,
        tool_names_for_seeds,
        arg_specs_for_seeds,
        tool_descs_for_seeds,
    )

    # TODO: remove
    all_variants = all_variants[:5]

    flat_prompts   = [v for variants in all_variants for v in variants]
    flat_toolnames = [
        _camel_to_snake(
            spec["paths"][p][m].get("operationId") or f"{m}_{p.strip('/')}"
        )
        for (p, m, _), variants in zip(meta, all_variants)
        for _ in variants
    ]
    flat_argspecs  = [
        _build_arg_spec(p, m, spec)
        for (p, m, _), variants in zip(meta, all_variants)
        for _ in variants
    ]
    flat_descs = [
        op.get("description", "") or op.get("summary", "")
        for path, ops in spec.get("paths", {}).items()
        for method, op in ops.items()
        for _ in range(num_prompts)
    ]

    flat_paths = [
        p for (p, m, _), variants in zip(meta, all_variants) for _ in variants
    ]
    flat_methods = [
        m for (p, m, _), variants in zip(meta, all_variants) for _ in variants
    ]

    flat_triplets = _generate_tool_outputs_bulk(
        flat_prompts,
        flat_toolnames,
        flat_argspecs,
        flat_descs,
        flat_paths,
        flat_methods,
        agent_dir=os.path.dirname(dest_dir),   # ← pass path where agent.py lives
        mcp_name=mcp_name,                     # NEW
    )
    triplet_iter  = iter(flat_triplets)   # each: (args_json, tool_output, answer)

    tool_names = [
        _camel_to_snake(
            spec["paths"][path][method].get("operationId") or f"{method}_{path.strip('/')}"
        )
        for (path, method, _), variants in zip(meta, all_variants)
    ]
    outs_list = []
    trajs_list = []
    all_variants_out = []
    for (path, method, _), prompt_variants in zip(meta, all_variants):
        tool_name = _camel_to_snake(
            spec["paths"][path][method].get("operationId") or f"{method}_{path.strip('/')}"
        )
        trajs = []
        outs  = []
        for variant in prompt_variants:
            args_json, tool_out, answer = next(triplet_iter)
            trajs.append(
                _mk_trajectory(
                    variant,
                    tool_name,
                    args_json,
                    tool_out,
                    answer,
                    mcp_name,             # ← MCP server’s name
                )
            )
            outs.append(answer)
        outs_list.append(outs)
        trajs_list.append(trajs)
        all_variants_out.append(prompt_variants)

    # 2. create YAML dataset and driver -------------------------------------------
    yaml_cases = []
    for idx, (tool_name, prompt_variants, outs, trajs) in enumerate( zip(tool_names, all_variants_out, outs_list, trajs_list) ):
        for j, (p, ans, tr) in enumerate(zip(prompt_variants, outs, trajs)):
            args_entry = tr[1]["tool_calls"][0]["function"]["arguments"] if tr[1].get("tool_calls") else {}
            args_dict  = (
                args_entry
                if isinstance(args_entry, dict)
                else (json.loads(args_entry) if args_entry else {})
            )
            yaml_cases.append(
                {
                    "id": f"tc_{idx}_{j}",
                    "prompt": p,
                    "answer": ans,
                    "reference_traj": yaml.safe_dump(tr, sort_keys=False),
                    "tool_name": tool_name,
                    "arguments_yaml": yaml.safe_dump(args_dict, sort_keys=False),
                }
            )

    from jinja2 import Environment, FileSystemLoader
    from pathlib import Path

    env = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parent.parent / "templates" / "agent" / "eval")))
    with open(os.path.join(dest_dir, "dataset.yaml"), "w", encoding="utf-8") as fp:
        fp.write(env.get_template("dataset.tpl").render(tests=yaml_cases))
    with open(os.path.join(dest_dir, "evaluate_agent.py"), "w", encoding="utf-8") as fp:
        fp.write(env.get_template("evaluate_agent.tpl").render(mcp_name=mcp_name))

    # 3. create __init__.py marker -------------------------------------------------
    with open(os.path.join(dest_dir, "__init__.py"), "w", encoding="utf-8") as fp:
        fp.write("")

    # 4. tell the generator we are done
    print(f"✅   Evaluation suite written to: {dest_dir}")
