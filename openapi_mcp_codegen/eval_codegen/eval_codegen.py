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
    tool_func_map: dict[str, Any] = {}

    tools_pkg = importlib.import_module(f"{pkg_name}.tools")
    for _, modname, _ in pkgutil.walk_packages(tools_pkg.__path__):
        mod = importlib.import_module(f"{pkg_name}.tools.{modname}")
        for name, obj in inspect.getmembers(mod):
            if inspect.iscoroutinefunction(obj) or callable(obj):
                tool_func_map[name] = obj

    import re  # already imported at top; keep if present

    def _lookup_tool(name: str):
        """Return the generated function that matches *name* best.

        Normalisation steps:
          • replace '/', '.', '-' with '_'
          • drop the '{' and '}' characters that wrap path-params
        """
        if name in tool_func_map:
            return tool_func_map[name]

        # 1) simple delimiter replacement
        cand = re.sub(r"[./-]", "_", name)
        if cand in tool_func_map:
            return tool_func_map[cand]

        # 2) additionally strip curly braces
        cand2 = cand.replace("{", "").replace("}", "")
        if cand2 in tool_func_map:
            return tool_func_map[cand2]

        raise KeyError(
            f"Tool function {name!r} not found "
            f"(tried {cand!r} and {cand2!r}). "
            f"Available: {sorted(tool_func_map)[:20]}..."
        )

    from langchain_core.messages import (
        AIMessage,
        ToolMessage,
        SystemMessage,
        HumanMessage,
    )
    from langgraph.errors import GraphRecursionError   # NEW
    import uuid
    from agentevals.graph_trajectory.utils import extract_langgraph_trajectory_from_thread

    async def _agent_runner():
        """Run all prompt/tool pairs in parallel and preserve order."""

        async def _process(prompt: str, tool: str) -> tuple[list[Any], str]:
            """
            Drive a multi-turn conversation until the “user-LLM” is satisfied.

            Returns:
              trajectory_msgs – list obtained via
                extract_langgraph_trajectory_from_thread(...)
              final_answer    – last assistant free-text reply.
            """
            user_llm = LLMFactory().get_llm()
            msg = [{"role": "user", "content": prompt}]

            # Build agent once and reuse same thread for all turns ----------
            thread_id = uuid.uuid4().hex
            cfg = {"configurable": {"thread_id": thread_id}}
            agent = await create_agent(tools=[_lookup_tool(tool)])

            for _ in range(2):  # ≤ 10 conversation turns
                try:
                    result = await agent.ainvoke({"messages": msg}, cfg)
                    msgs   = result["messages"]
                except GraphRecursionError as e:
                    # Return whatever we have so far
                    traj = extract_langgraph_trajectory_from_thread(agent, cfg)
                    return traj, f"[Graph recursion limit reached] {e}"

                # Assistant’s latest natural-language reply (no tool_calls)
                answer = next(
                    (m.content for m in reversed(msgs)
                     if isinstance(m, AIMessage) and not m.tool_calls),
                    "",
                )

                # Ask user-LLM whether satisfied ---------------------------
                sat_prompt = (
                    "You are the end-user. The assistant just replied:\n"
                    f"{answer}\n\n"
                    'If you are satisfied, answer exactly: "Thank you, that is all." '
                    "Otherwise rewrite your request only."
                )
                user_reply = (
                    await user_llm.ainvoke([SystemMessage(sat_prompt)])
                ).content.strip()

                if user_reply.lower().startswith("thank you"):
                    break  # conversation complete
                msg = [{"role": "user", "content": user_reply + " Please try again."}]

            # Extract full LangGraph trajectory for this thread -------------
            trajectory_msgs = extract_langgraph_trajectory_from_thread(agent, cfg)
            return trajectory_msgs, answer

        tasks = [
            _process(p, t) for p, t in zip(prompts, tool_names)
        ]
        return await asyncio.gather(*tasks)

    return asyncio.run(_agent_runner())


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
    num_prompts: int,
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
    # all_variants = all_variants[:10]

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

    flat_pairs = _generate_tool_outputs_bulk(
        flat_prompts,
        flat_toolnames,
        flat_argspecs,
        flat_descs,
        flat_paths,
        flat_methods,
        agent_dir=os.path.dirname(dest_dir),   # ← pass path where agent.py lives
        mcp_name=mcp_name,                     # NEW
    )
    pair_iter = iter(flat_pairs)        # each item: (trajectory_msgs, answer)

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
            traj_dicts, answer = next(pair_iter)
            trajs.append(traj_dicts)
            outs.append(answer)
        outs_list.append(outs)
        trajs_list.append(trajs)
        all_variants_out.append(prompt_variants)

    # 2. create YAML dataset and driver -------------------------------------------
    yaml_cases = []
    for idx, (tool_name, prompt_variants, outs, trajs) in enumerate( zip(tool_names, all_variants_out, outs_list, trajs_list) ):
        for j, (p, ans, tr) in enumerate(zip(prompt_variants, outs, trajs)):
            print(tr)
            yaml_cases.append(
                {
                    "id": f"tc_{idx}_{j}",
                    "prompt": p,
                    "answer": ans,
                    "reference_traj": yaml.safe_dump(tr, sort_keys=False),
                    "tool_name": tool_name,
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
