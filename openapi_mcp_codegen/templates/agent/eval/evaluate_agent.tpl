"""
Standalone evaluation script for the generated {{ mcp_name }} agent.
Loads YAML test cases and computes trajectory-match, correctness, hallucination.
"""

import asyncio, yaml, os, sys, json
from pathlib import Path
from typing import List, Dict
import uuid

from langsmith import aevaluate
from langsmith.schemas import Run, Example
from langsmith import Client

sys.path.append(str(Path(__file__).parent.parent))  # make agent importable

from agentevals.trajectory.match import create_trajectory_match_evaluator
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT
from cnoe_agent_utils import LLMFactory
from agent import create_agent
DATASET = Path(__file__).with_name("dataset.yaml")

_AGENT = asyncio.run(create_agent())

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
        traj   = data["reference_trajectory"]["solution_1"].split(";")
        det_traj = [{"role": "system", "agent": n, "content": ""} for n in traj]
        items.append({"id": tid, "input": data["input"], "ref_out": data["reference_output"], "ref_traj": det_traj})
    return items

async def predict(inputs):
    prompt = inputs["prompt"]
    traj, outputs = await _run_agent(_AGENT, prompt)
    # Store everything aevaluate-needs as outputs
    return {"traj": traj, "outputs": outputs}

STRICT  = create_trajectory_match_evaluator(trajectory_match_mode="strict")
UNORDER = create_trajectory_match_evaluator(trajectory_match_mode="unordered")

async def metric_traj_match(run: Run, example: Example):
    ok = UNORDER(outputs=run.outputs["traj"], reference_outputs=example.outputs["ref_traj"])["score"] or \
         STRICT(outputs=run.outputs["traj"],  reference_outputs=example.outputs["ref_traj"])["score"]
    return {"key": "traj_match", "score": 1 if ok else 0}

async def metric_correctness(run: Run, example: Example):
    score = CORR(inputs=example.inputs["prompt"], outputs=run.outputs["outputs"], reference_outputs=example.outputs["ref_out"])["score"]
    return {"key": "correctness", "score": score}

async def metric_hallucination(run: Run, example: Example):
    score = HALLU(inputs=example.inputs["prompt"], outputs=run.outputs["outputs"], context=example.outputs["ref_traj"], reference_outputs=example.outputs["ref_out"])["score"]
    return {"key": "hallucination", "score": score}

async def main():
    cases = load_dataset()

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
        evaluators=[metric_traj_match, metric_correctness, metric_hallucination],
        experiment_prefix="agent_eval",
        max_concurrency=None,
    )

if __name__ == "__main__":
    asyncio.run(main())
