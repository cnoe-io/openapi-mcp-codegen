"""
Standalone evaluation script for the generated {{ mcp_name }} agent.
Loads YAML test cases and computes trajectory-match, correctness, hallucination.
"""

import asyncio, yaml, os, sys, json
from pathlib import Path
from typing import List, Dict, Any
import uuid

from langsmith import aevaluate
from langsmith.schemas import Run, Example
from langsmith import Client
from agentevals.graph_trajectory.utils import (
    extract_langgraph_trajectory_from_thread,
)

from agentevals.graph_trajectory.llm import create_graph_trajectory_llm_as_judge
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT
from cnoe_agent_utils import LLMFactory

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def _ref(example: Example, key: str):
    """
    LangSmith returns `Example.outputs` as a *list* of dicts.
    This helper always returns example.outputs[0][key].
    """
    out = example.outputs
    if isinstance(out, list):
        return out[0].get(key)
    return out.get(key)

sys.path.append(str(Path(__file__).parent.parent))  # make agent importable

# Import create_agent and the shared DEFAULT_SYSTEM_PROMPT
try:
    from agent import create_agent, DEFAULT_SYSTEM_PROMPT
except ImportError:
    from {{ mcp_name }}.agent import create_agent, DEFAULT_SYSTEM_PROMPT
DATASET = Path(__file__).with_name("dataset.yaml")

_AGENT = None

CORR    = create_llm_as_judge(prompt=CORRECTNESS_PROMPT,   feedback_key="correctness",   judge=LLMFactory().get_llm())
HALLU   = create_llm_as_judge(prompt=HALLUCINATION_PROMPT, feedback_key="hallucination", judge=LLMFactory().get_llm())

async def _run_agent(agent, prompt: str):
    logger.debug("Invoking agent for prompt: %s", prompt)
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    # invoke with user prompt
    await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]}, config=cfg)
    # extract graph trajectory for later judging
    traj = extract_langgraph_trajectory_from_thread(agent, cfg)
    # collect assistant texts from the LangGraph trajectory itself
    outputs: list[str] = []
    for step in traj.get("results", []):
        for msg in step.get("messages", []):
            if msg.get("role") == "assistant":
                outputs.append(msg.get("content", ""))
    logger.debug("Received %d assistant messages", len(outputs))
    return traj, outputs

def load_dataset() -> List[Dict]:
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
    logger.info("Loading dataset from %s", DATASET)
    with open(DATASET, encoding="utf-8") as fp:
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
    # Store everything aevaluate-needs as outputs
    return {"traj": traj, "outputs": outputs}

TRAJ_ACC = create_graph_trajectory_llm_as_judge(judge=LLMFactory().get_llm())

async def metric_graph_traj_accuracy(run: Run, example: Example):
    """
    Use LLM judge to compare the LangGraph trajectory produced by the agent
    (run.outputs["traj"]) with the reference trajectory stored in the dataset.
    """
    ref_traj = _ref(example, "ref_traj")
    pred_traj = run.outputs["traj"]
    return TRAJ_ACC(
        inputs=ref_traj["inputs"],      # reference user / tool calls
        outputs=pred_traj["outputs"],   # agent-generated calls
    )

async def metric_correctness(run: Run, example: Example):
    ref_out = _ref(example, "ref_out")
    score = CORR(
        inputs=example.inputs["prompt"],
        outputs=run.outputs["outputs"],
        reference_outputs=ref_out
    )["score"]
    return {"key": "correctness", "score": score}

async def metric_hallucination(run: Run, example: Example):
    ref_out = _ref(example, "ref_out")
    score = HALLU(
        inputs=example.inputs["prompt"],
        outputs=run.outputs["outputs"],
        context="",
        reference_outputs=ref_out
    )["score"]
    return {"key": "hallucination", "score": score}

async def main():
    logger.info("=== Agent evaluation started ===")
    cases = load_dataset()
    global _AGENT
    logger.info("Bootstrapping agent instance …")
    _AGENT, _ = await create_agent(prompt=DEFAULT_SYSTEM_PROMPT)

    # 2. Create / reuse a LangSmith dataset
    dataset_name = "{{ mcp_name }}_agent_eval"
    client = Client()

    inputs, outputs = [], []
    for c in cases:
        inputs.append({"prompt": c["input"]})
        outputs.append({"ref_traj": c["ref_traj"], "ref_out": c["ref_out"]})

    try:
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=f"Evaluation dataset for {{ mcp_name }} agent",
        )
        client.create_examples(
            inputs=inputs,
            outputs=outputs,
            dataset_id=dataset.id,
        )
    except Exception as e:
        # Dataset probably already exists – that is fine.
        print(e)

    # 3. Run evaluation using the (remote) dataset name
    logger.info("Running evaluations via LangSmith …")
    await aevaluate(
        predict,
        data=dataset_name,   #  ← pass dataset name, not local Examples
        evaluators=[metric_graph_traj_accuracy, metric_correctness, metric_hallucination],
        experiment_prefix="agent_eval",
        max_concurrency=None,
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        logger.info("=== Agent evaluation finished ===")
