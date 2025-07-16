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


async def _llm_tool_output_async(
    llm,
    prompt: str,
    tool_name: str,
    arg_spec: str,
    tool_desc: str,
) -> tuple[str, str, str]:
    """
    Given the *user prompt*, produce:
      • JSON string with function arguments,
      • JSON string with a plausible tool response,
      • assistant answer text.
    Returns (args_json, tool_output_json, answer_text).
    """
    if not hasattr(llm, "ainvoke"):
        return "{}", "{}", f"[ANSWER] call to {tool_name}"

    sys_msg = SystemMessage(
        content=(
            "You simulate both the caller and backend of a Komodor API, a Kubernetes management platform.\n"
            f"Tool/function: {tool_name}\n"
            f"Tool description: {tool_desc}\n"
            f"Argument schema: {arg_spec}\n\n"
            "For the **USER REQUEST** below:\n"
            "  1) craft concrete JSON arguments matching the schema;\n"
            "  2) invent a realistic JSON response from the backend;\n"
            "  3) write the assistant's natural-language reply.\n\n"
            "Return ONLY a JSON object with keys:\n"
            '  "args":        <JSON object>,\n'
            '  "tool_output": <JSON object>,\n'
            '  "answer":      <string>\n'
            "No markdown, no code-fences."
        )
    )
    resp = await llm.ainvoke([sys_msg, SystemMessage(prompt)])
    try:
        data = json.loads(resp.content)
        return (
            json.dumps(data.get("args", {}),        ensure_ascii=False),
            json.dumps(data.get("tool_output", {}), ensure_ascii=False),
            data.get("answer", "").strip(),
        )
    except Exception:
        # Fallback: empty args/output, raw content as answer
        return "{}", "{}", resp.content.strip()

def _generate_tool_outputs_bulk(
    prompts:    List[str],
    tool_names: List[str],
    arg_specs:  List[str],
    tool_descs: List[str],
) -> List[tuple[str, str, str]]:
    llm = LLMFactory().get_llm()
    async def _runner():
        return await asyncio.gather(
            *[
                _llm_tool_output_async(llm, p, t, s, d)
                for p, t, s, d in zip(prompts, tool_names, arg_specs, tool_descs)
            ],
            return_exceptions=False,
        )
    return asyncio.run(_runner())




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

    flat_triplets = _generate_tool_outputs_bulk(
        flat_prompts,
        flat_toolnames,
        flat_argspecs,
        flat_descs,
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
    # TODO: remove
    yaml_cases = yaml_cases[:10]

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
