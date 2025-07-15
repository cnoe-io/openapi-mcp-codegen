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
from cnoe_agent_utils import LLMFactory
from langchain_core.messages import SystemMessage

def _camel_to_snake(name: str) -> str:
    out = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    out = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", out)
    return out.replace("-", "_").lower()


async def _llm_ref_async(llm, prompt: str, tool_name: str) -> tuple[str, str]:
    """
    Ask LLM for JSON arguments **and** final answer for *tool_name* given *prompt*.
    Returns (arguments_json_str, assistant_answer).
    On failure, returns fallback stub.
    """
    if not hasattr(llm, "ainvoke"):
        return "{}", f"[REFERENCE] {prompt}"

    system = SystemMessage(
        content=(
            "You are an API-aware assistant. For the user request below you must:"
            " 1) decide arguments for calling the function '{tool_name}'."
            " 2) compose a natural-language answer for the user."
            "Return ONLY a JSON object with two keys:\n"
            '  "arguments": <JSON dict for the call>\n'
            '  "answer":    <assistant reply string>.\n'
            "No markdown, no code fences."
        ).format(tool_name=tool_name)
    )
    resp = await llm.ainvoke([system, SystemMessage(prompt)])
    try:
        data = json.loads(resp.content)
        return json.dumps(data.get("arguments", {}), ensure_ascii=False), data.get("answer", "").strip()
    except Exception:
        return "{}", resp.content.strip()


def _generate_reference_bulk(prompts: List[str], tool_names: List[str]) -> List[tuple[str, str]]:
    """
    Concurrently obtain (arguments_json, assistant_answer) for each prompt/tool pair.
    """
    llm = LLMFactory().get_llm()

    async def runner():
        res = await asyncio.gather(
            *[_llm_ref_async(llm, p, t) for p, t in zip(prompts, tool_names)],
            return_exceptions=True,
        )
        for r in res:
            if isinstance(r, Exception):
                raise r
        return res

    return asyncio.run(runner())


def _mk_trajectory(user_prompt: str, tool_name: str, args_json: str, answer: str) -> List[Dict[str, Any]]:
    call_id = uuid.uuid4().hex
    return [
        {"role": "user", "agent": "__start__", "content": user_prompt},
        {
            "role": "assistant",
            "agent": "reference_agent",
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "id": call_id,
                    "function": {"name": tool_name, "arguments": args_json},
                }
            ],
        },
        {
            "role": "tool",
            "agent": "mcp_tools",
            "content": "REFERENCE_TOOL_OUTPUT",
            "tool_call_id": call_id,
        },
        {"role": "assistant", "agent": "reference_agent", "content": answer},
    ]

async def _llm_variations_async(llm, seed: str, n: int) -> List[str]:
    """
    Async helper that asks the LLM for *n* paraphrases of *seed*.
    Falls back to deterministic stubs if LLM is unavailable.
    """
    if not hasattr(llm, "ainvoke"):  # stub or sync-only LLM
        return [f"{seed} (variant {i+1})" for i in range(n)]

    prompt = (
        f"Produce {n} different phrasings of the following instruction, "
        f"return as a JSON list only (no markdown): '{seed}'"
    )
    resp = await llm.ainvoke([SystemMessage(prompt)])
    try:
        return json.loads(resp.content)
    except Exception:
        return [line.strip("- ") for line in resp.content.split("\n") if line.strip()][:n]


def _generate_variations_bulk(seeds: List[str], n: int) -> List[List[str]]:
    """
    Create paraphrases for *seeds* concurrently using a single event loop.
    Returns a list parallel to *seeds* where each element is the list of n variants.
    """
    llm = LLMFactory().get_llm()

    async def _runner():
        results = await asyncio.gather(
            *[_llm_variations_async(llm, seed, n) for seed in seeds],
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
    cases: List[Dict[str, Any]] = []

    seeds: List[str] = []
    meta:  List[tuple[str, str, str]] = []   # (path, method, summary) for later alignment
    for path, ops in spec.get("paths", {}).items():
        for method, op in ops.items():
            summary = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
            seed_prompt = f"{summary} using the {mcp_name} tools"
            seeds.append(seed_prompt)
            meta.append((path, method, summary))

    all_variants = _generate_variations_bulk(seeds, num_prompts)

    ref_pairs = _generate_reference_bulk(
        [v for variants in all_variants for v in variants],
        [ _camel_to_snake(op.get("operationId") or f"{m}_{p.strip('/')}")
          for (p, m, _), variants in zip(meta, all_variants)
          for _ in variants ],
    )
    flat_iter = iter(ref_pairs)

    for (path, method, _), prompt_variants in zip(meta, all_variants):
        tool_name = _camel_to_snake(
            spec["paths"][path][method].get("operationId") or f"{method}_{path.strip('/')}"
        )
        trajs = []
        outs  = []
        for variant in prompt_variants:
            args_json, answer = next(flat_iter)
            trajs.append(_mk_trajectory(variant, tool_name, args_json, answer))
            outs.append(answer)
        cases.append(
            {"input": prompt_variants, "output": outs, "trajectories": trajs}
        )

    with open(os.path.join(dest_dir, "generated_prompts.json"), "w", encoding="utf-8") as fp:
        json.dump(cases, fp, indent=2, ensure_ascii=False)

    # 2. create __init__.py marker -------------------------------------------------
    with open(os.path.join(dest_dir, "__init__.py"), "w", encoding="utf-8") as fp:
        fp.write("")

    # 3. generate pytest harness ---------------------------------------------------
    from jinja2 import Environment, FileSystemLoader
    from pathlib import Path

    tmpl_env = Environment(
        loader=FileSystemLoader(
            str(
                Path(__file__).resolve().parent.parent
                / "templates"
                / "agent"
                / "eval"
            )
        )
    )
    harness_code = tmpl_env.get_template("test_agent_eval.tpl").render()
    # write the test one level above `eval/` (same dir as agent.py)
    harness_path = os.path.join(os.path.dirname(dest_dir), "test_agent_eval.py")
    with open(harness_path, "w", encoding="utf-8") as fp:
        fp.write(harness_code)

    # 4. tell the generator we are done
    print(f"✅   Evaluation suite written to: {dest_dir}")
