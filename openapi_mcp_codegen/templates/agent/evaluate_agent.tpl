"""
Standalone evaluation script for the generated {{ mcp_name }} agent.
Loads YAML test cases and computes trajectory-match, correctness, hallucination.
"""

import asyncio, yaml, os, sys
from pathlib import Path
from typing import List, Dict, Any
import uuid

from agentevals.graph_trajectory.utils import (
    extract_langgraph_trajectory_from_thread,
)

from agentevals.graph_trajectory.llm import create_graph_trajectory_llm_as_judge
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT
from cnoe_agent_utils import LLMFactory
from langfuse import get_client
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


sys.path.append(str(Path(__file__).parent.parent))  # make agent importable

# Import create_agent and the shared DEFAULT_SYSTEM_PROMPT
try:
    from agent import create_agent, DEFAULT_SYSTEM_PROMPT
except ImportError:
    from {{ mcp_name }}.agent import create_agent, DEFAULT_SYSTEM_PROMPT
DEFAULT_DATASET = Path(__file__).with_name("dataset.yaml")

_AGENT = None

CORR    = create_llm_as_judge(prompt=CORRECTNESS_PROMPT,   feedback_key="correctness",   judge=LLMFactory().get_llm())
HALLU   = create_llm_as_judge(prompt=HALLUCINATION_PROMPT, feedback_key="hallucination", judge=LLMFactory().get_llm())

async def _run_agent(agent, prompt: str):
    logger.debug("Invoking agent for prompt: %s", prompt)
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    lf_handler = None
    try:
        lf_handler = LangfuseCallbackHandler()
    except Exception:
        pass
    langfuse = get_client()
    with langfuse.start_as_current_span(
        name="{{ mcp_name }}-predict",
        input={"prompt": prompt},
    ) as span:
        await agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config={**cfg, "callbacks": ([lf_handler] if lf_handler else [])},
        )
        # extract graph trajectory for later judging
        traj = extract_langgraph_trajectory_from_thread(agent, cfg)
        # collect assistant texts from the LangGraph trajectory itself
        outputs: list[str] = []
        for step in traj["outputs"]["results"]:
            for msg in step.get("messages", []):
                if msg.get("role") == "assistant":
                    outputs.append(msg.get("content", ""))
        span.update_trace(output={"outputs": "\n".join(outputs)})
    logger.debug("Received %d assistant messages", len(outputs))
    return traj, "\n".join(outputs)

def load_dataset(ds_path: Path) -> List[Dict]:
    """
    Read eval/dataset.yaml created by eval_mode.py.

    Expected YAML structure:
      tests:
        - tool: <name>
          input:  <user prompt>
          output: <assistant text>
          trajectory: <list of messages>
        - tool: <name>          # skipped tools have only this key
    """
    logger.info("Loading dataset from %s", ds_path)
    with open(ds_path, encoding="utf-8") as fp:
        raw = yaml.safe_load(fp) or {}

    tests = raw.get("tests", []) or []
    items: List[Dict] = []

    for idx, entry in enumerate(tests):
        # ignore skipped-only entries
        if not all(k in entry for k in ("input", "output", "trajectory")):
            continue

        items.append(
            {
                "id": f"{entry.get('tool','case')}_{idx}",
                "input": entry["input"],
                "ref_out": entry["output"],
                "ref_traj": entry["trajectory"],
            }
        )

    logger.info("Loaded %d usable test cases", len(items))
    return items

async def predict(inputs):
    prompt = inputs["prompt"]
    traj, outputs = await _run_agent(_AGENT, prompt)
    try:
        lf = get_client()
        with lf.start_as_current_span(name="{{ mcp_name }}-predict") as span:
            span.update_trace(input={"prompt": prompt}, output={"outputs": outputs})
    except Exception:
        pass
    # Store everything aevaluate-needs as outputs
    return {"traj": traj, "outputs": outputs}

TRAJ_ACC = create_graph_trajectory_llm_as_judge(judge=LLMFactory().get_llm())

async def metric_graph_traj_accuracy(pred: dict, example: dict):
    """
    Compare the agent-generated trajectory (pred["traj"]) with the reference one
    contained in `example["ref_traj"]` using an LLM judge.
    """
    ref_traj = example["ref_traj"]
    pred_traj = pred["traj"]
    return TRAJ_ACC(
        inputs=ref_traj["inputs"],      # reference user / tool calls
        outputs=pred_traj["outputs"],   # agent-generated calls
    )

async def metric_correctness(pred: dict, example: dict):
    """
    Judge textual correctness of the agent response compared to the reference
    answer stored in the dataset entry.
    """
    return CORR(
        inputs=example["input"],
        outputs=pred["outputs"],
        reference_outputs=example["ref_out"],
    )

async def metric_hallucination(pred: dict, example: dict):
    """
    Judge hallucination: does the agent output contain unsupported claims?
    """
    return HALLU(
        inputs=example["input"],
        outputs=pred["outputs"],
        context="",
        reference_outputs=example["ref_out"],
    )

async def main():
    logger.info("=== Agent evaluation started ===")
    lf = get_client()
    try:
        with lf.start_as_current_span(name="{{ mcp_name }}-eval") as init_span:
            init_span.update_trace(tags=["{{ mcp_name }}-eval"])
    except Exception:
        pass
    # --------------------------------------------------------- dataset selection prompt
    try:
        ds_input = input(f"Path to dataset YAML [default: {DEFAULT_DATASET}]: ").strip()
    except Exception:
        ds_input = ""
    dataset_path = (Path(ds_input).expanduser().resolve() if ds_input else DEFAULT_DATASET)
    cases = load_dataset(dataset_path)
    global _AGENT
    logger.info("Bootstrapping agent instance …")
    _AGENT, _ = await create_agent(prompt=DEFAULT_SYSTEM_PROMPT)

    # -------------------------------------------------------------- Langfuse dataset + runs
    lf = get_client()
    dataset_name = "{{ mcp_name }}_agent_eval"
    run_name = f"{{ mcp_name }}_agent_eval_run_{uuid.uuid4().hex[:8]}"

    try:
        dataset = lf.get_dataset(name=dataset_name)
    except Exception:
        dataset = lf.create_dataset(
            name=dataset_name,
            description="Evaluation dataset for {{ mcp_name }} agent",
        )

    # ------------------------------------------------------------------ per-item worker
    async def _process_case(c: dict):
        """
        Process one evaluation case:
        1. Ensure Langfuse dataset + item exist.
        2. Create a run context/span.
        3. Invoke the agent, compute metrics and record scores.
        4. Trigger Langfuse async API fetch for the created trace id.
        """
        item_input = {"prompt": c["input"]}
        expected_output = {"ref_traj": c["ref_traj"], "ref_out": c["ref_out"]}

        # Ensure dataset item exists (ignore error if duplicate)
        try:
            lf.create_dataset_item(
                dataset_name=dataset_name,
                input=item_input,
                expected_output=expected_output,
            )
        except Exception:
            pass

        # Obtain the dataset and its items (v3 API)
        try:
            dataset_obj = lf.get_dataset(name=dataset_name)
            ds_item = next(
                (it for it in getattr(dataset_obj, "items", []) if it.input == item_input),
                None,
            )
        except Exception:
            ds_item = None

        if ds_item and hasattr(ds_item, "run"):
            run_ctx = ds_item.run(
                run_name=run_name,
                run_metadata={"agent": "{{ mcp_name }}"},
                run_description=f"Evaluation run for {{ mcp_name }}",
            )
        else:
            # Fallback: create a root span if linking fails
            run_ctx = lf.start_as_current_span(
                name=f"{{ mcp_name }}-eval-item",
                input=item_input,
            )

        # ------------------------------ execute + score inside the run span
        with run_ctx as root_span:  # type: ignore[assignment]
            pred = await predict(item_input)
            root_span.update_trace(input=item_input, output={"outputs": pred["outputs"]})

            # Fire-and-forget call to Langfuse async API for this trace
            try:
                trace_id = root_span.trace_id
                await lf.async_api.trace(trace_id)
            except Exception:
                pass

            traj_acc = await metric_graph_traj_accuracy(pred, {"ref_traj": c["ref_traj"]})
            corr     = await metric_correctness(pred, {"input": c["input"], "ref_out": c["ref_out"]})
            hallu    = await metric_hallucination(pred, {"input": c["input"], "ref_out": c["ref_out"]})

            root_span.score_trace(name="trajectory_accuracy", value=float(traj_acc.get("score", 0.0)))
            root_span.score_trace(name="correctness",          value=float(corr.get("score", 0.0)))
            root_span.score_trace(name="hallucination",        value=float(hallu.get("score", 0.0)))

    # Kick-off all evaluations concurrently
    tasks = [_process_case(c) for c in cases]
    await asyncio.gather(*tasks)

    # Flush Langfuse traces
    try:
        get_client().flush()
    except Exception:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        logger.info("=== Agent evaluation finished ===")
