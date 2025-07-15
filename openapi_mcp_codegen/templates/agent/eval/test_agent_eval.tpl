import asyncio
import json
import random
import sys
from pathlib import Path

import os
os.environ["MOCK_API"] = "1"

from agentevals.trajectory.match import create_trajectory_match_evaluator
from langsmith import testing as t
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT
from cnoe_agent_utils import LLMFactory

# -------------------------------------------------------------------- import generated agent ----
from agent import create_agent                    # noqa: E402

# -------------------------------------------------------------------- constants -----------------
DATA_FILE = str(Path(__file__).parent / "eval" / "generated_prompts.json")

STRICT_EVAL    = create_trajectory_match_evaluator(trajectory_match_mode="strict")
UNORDERED_EVAL = create_trajectory_match_evaluator(trajectory_match_mode="unordered")

CORRECTNESS = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    judge=LLMFactory().get_llm(),
)
HALLUCINATION = create_llm_as_judge(
    prompt=HALLUCINATION_PROMPT,
    feedback_key="hallucination",
    judge=LLMFactory().get_llm(),
)

# -------------------------------------------------------------------- helpers -------------------
async def _trajectory_for_prompt(prompt: str):
    """
    Invoke the generated LangGraph agent and return:
      • full LangGraph message trajectory
      • list of assistant outputs (plain text) extracted from that trajectory
    """
    agent = await create_agent()
    cfg = {"configurable": {"thread_id": "eval-session"}}
    try:
        result = await agent.ainvoke({"messages": [("user", prompt)]}, cfg)
    except Exception as e:
        raise RuntimeError(f"Agent invocation failed for prompt '{prompt}': {e}") from e

    messages = result.get("messages", [])
    # Grab contents of assistant role messages
    outputs = [m.content for m in messages if getattr(m, "role", "") == "assistant"]
    return messages, outputs

# -------------------------------------------------------------------- dataset -------------------
with open(DATA_FILE, encoding="utf-8") as fp:
    DATA = json.load(fp)

TRIPLETS = []
for item in DATA:
    for prompt, answer, traj in zip(
        item["input"],            # prompt variants
        item["output"],           # matching reference answers
        item["trajectories"],     # matching reference trajectories
    ):
        TRIPLETS.append((prompt, [answer], traj))

random.seed(42)
SAMPLE = random.sample(TRIPLETS, min(5, len(TRIPLETS)))  # keep CI fast

# -------------------------------------------------------------------- tests ---------------------
import pytest

@pytest.mark.langsmith(output_keys=["user_input", "reference_outputs", "reference_trajectory"])
@pytest.mark.parametrize("user_input,reference_outputs,reference_trajectory", SAMPLE)
def test_trajectory_accuracy(user_input, reference_outputs, reference_trajectory):
    trajectory, outputs = asyncio.run(_trajectory_for_prompt(user_input))

    t.log_inputs({"user input": user_input,"trajectory":trajectory})
    t.log_outputs({"outputs": outputs})
    t.log_reference_outputs({"reference_outputs": reference_outputs})

    unordered = UNORDERED_EVAL(outputs=trajectory, reference_outputs=reference_trajectory)
    strict    = STRICT_EVAL(outputs=trajectory,    reference_outputs=reference_trajectory)
    correctness  = CORRECTNESS(inputs=user_input, outputs=outputs, reference_outputs=reference_outputs)
    hallucination = HALLUCINATION(inputs=user_input, outputs=outputs, context=reference_trajectory, reference_outputs=reference_outputs)

    score = (unordered["score"] or strict["score"]) and correctness["score"] and hallucination["score"]
    assert score
