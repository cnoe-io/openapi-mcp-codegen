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

sys.path.append(str(Path(__file__).parent.parent))  # make agent importable

from agentevals.trajectory.llm import (
    create_trajectory_llm_as_judge,
    TRAJECTORY_ACCURACY_PROMPT,
)
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT
from cnoe_agent_utils import LLMFactory
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
    res = await agent.ainvoke({"messages": [("user", prompt)]}, config={"configurable": {"thread_id": uuid.uuid4().hex}})
    msgs = res["messages"]
    outputs = [m.content for m in msgs if getattr(m, "role", "") == "assistant"]
    return msgs, outputs

def load_dataset() -> List[Dict]:
    with open(DATASET, encoding="utf-8") as fp:
        raw = yaml.safe_load(fp)
    items = []
    for tid, data in raw["tests"].items():
        det_traj = data["reference_trajectory"]                 # now native YAML list
        # det_traj is a list-of-dicts already
        # ref_out = next((m["content"] for m in reversed(det_traj) if m.get("role") == "assistant"), "")
        ref_out = data["output"]
        items.append({"id": tid, "input": data["input"], "ref_out": ref_out, "ref_traj": det_traj})
    return items

async def predict(inputs):
    prompt = inputs["prompt"]
    traj, outputs = await _run_agent(_AGENT, prompt)
    # Store everything aevaluate-needs as outputs
    return {"traj": traj, "outputs": outputs}

TRAJ_ACC = create_trajectory_llm_as_judge(
    prompt=TRAJECTORY_ACCURACY_PROMPT,
    feedback_key="trajectory_accuracy",
    judge=LLMFactory().get_llm(),
)

async def metric_traj_accuracy(run: Run, example: Example):
    """
    Uses an LLM judge to compare the agent-generated trajectory with the reference trajectory.
    Returns a continuous 0-1 score.
    """
    score = TRAJ_ACC(
        inputs=example.inputs["prompt"],
        outputs=run.outputs["traj"],
        reference_outputs=example.outputs["ref_traj"],
    )["score"]
    return {"key": "traj_accuracy", "score": score}

async def metric_correctness(run: Run, example: Example):
    score = CORR(inputs=example.inputs["prompt"], outputs=run.outputs["outputs"], reference_outputs=example.outputs["ref_out"])["score"]
    return {"key": "correctness", "score": score}

async def metric_hallucination(run: Run, example: Example):
    score = HALLU(inputs=example.inputs["prompt"], outputs=run.outputs["outputs"], context=example.outputs["ref_traj"], reference_outputs=example.outputs["ref_out"])["score"]
    return {"key": "hallucination", "score": score}

async def main():
    cases = load_dataset()
    global _AGENT
    _AGENT = await create_agent(prompt=DEFAULT_SYSTEM_PROMPT)

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
    await aevaluate(
        predict,
        data=dataset_name,   #  ← pass dataset name, not local Examples
        evaluators=[metric_traj_accuracy, metric_correctness, metric_hallucination],
        experiment_prefix="agent_eval",
        max_concurrency=None,
    )

if __name__ == "__main__":
    asyncio.run(main())
