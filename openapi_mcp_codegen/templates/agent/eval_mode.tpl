{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""Interactive evaluation mode for the {{ mcp_name | capitalize }} LangGraph agent.

Generates/updates eval/dataset.yaml with graph-trajectory traces for each tool.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

import yaml
from agentevals.graph_trajectory.utils import extract_langgraph_trajectory_from_thread

from agent import create_agent

from cnoe_agent_utils import LLMFactory
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)


def _prompt_for_query(
    tool_name: str,
    tool_desc: str,
    strategy: str,
    llm,
) -> tuple[str, str]:
    """
    Ask (and repeatedly re-ask) for a user query, allowing the evaluator to
    update the strategy.  Returns (user_query, updated_strategy).
    """
    # Print context
    if tool_desc:
        print(f"\nDescription: {tool_desc}")
    print(f"Using strategy: '{strategy or 'None'}'")

    def _suggest_query(cur_strategy: str) -> str:
        if not llm:
            return ""
        try:
            sys_msg = SystemMessage(
                content=(
                    "You are a senior QA engineer evaluating the functionality of API tools. "
                    "Given the tool name, its description and an optional evaluation strategy, "
                    "propose a concise natural-language user query to test the tool. "
                    "Respond with only the query."
                )
            )
            human_msg = HumanMessage(
                content=f"Tool: {tool_name}\nDescription: {tool_desc}\nStrategy: {cur_strategy}"
            )
            return llm.invoke([sys_msg, human_msg]).content.strip()
        except Exception as e:  # noqa: BLE001
            logger.warning("LLM suggestion failed: %s", e)
            return ""

    suggested_query = _suggest_query(strategy)

    while True:
        if suggested_query:
            print(f"Suggested query: {suggested_query}")

        inp = input(
            "Enter a user query "
            "(press Enter to accept suggestion, or (u)pdate strategy): "
        ).strip()

        if inp.lower() in ("u", "update"):
            strategy = input("Enter new evaluation strategy: ").strip()
            suggested_query = _suggest_query(strategy)
            continue

        return (inp or suggested_query), strategy


async def _interactive_eval() -> None:
    dataset_path = Path("eval/dataset.yaml")
    dataset_path.parent.mkdir(exist_ok=True, parents=True)

    # Load existing dataset (if any)
    dataset: Dict[str, Any] = []
    if dataset_path.exists():
        dataset = yaml.safe_load(dataset_path.read_text()).get("tests") or []

    # Optional global evaluation strategy (can be updated later)
    strategy = input(
        "Optional global evaluation strategy (e.g. resource names) – press Enter to skip: "
    ).strip()

    # Create one LLM instance for all query suggestions
    llm = None
    try:
        llm = LLMFactory().get_llm()
    except Exception as e:
        logger.warning("LLM init failed: %s", e)

    agent, tools = await create_agent()
    tool_map = {t.name: t for t in tools}
    all_tools = [t.name for t in tools]                          # full list
    completed_tools = {t["tool"] for t in dataset}              # already-evaluated tools
    remaining_tools = [t for t in all_tools if t not in completed_tools]

    while True:
        print("\nTools:")
        for idx, tool in enumerate(all_tools, start=1):
            marker = "(done)" if tool in completed_tools else ""
            print(f"{idx}. {tool} {marker}")
        # Prompt user – default is the next tool in the list
        default_tool = remaining_tools[0] if remaining_tools else all_tools[0]
        choice = input(
            f"Select tool to evaluate [{default_tool}] (enter/number/(s)kip): "
        ).strip()

        if choice == "":
            tool_name = default_tool
        elif choice.lower() in ("s", "skip"):
            if default_tool in remaining_tools:
                remaining_tools.remove(default_tool)
            continue
        elif choice.isdigit():
            idx = int(choice) - 1
            if not (0 <= idx < len(all_tools)):
                print("Invalid number, try again.")
                continue
            tool_name = all_tools[idx]
        else:
            print("Invalid input, enter a number, press Enter for default, or 's' to skip.")
            continue

        # ------------------------------------------------- dataset clash check
        existing_idx: list[int] = [
            i for i, t in enumerate(dataset) if t.get("tool") == tool_name
        ]
        replace_existing = False
        if existing_idx:
            choice = input(
                f"{len(existing_idx)} existing test(s) for '{tool_name}' found – "
                "(r)eplace or (a)dd as extra? [a]: "
            ).strip().lower()
            replace_existing = choice == "r"

        tool_desc = getattr(tool_map[tool_name], "description", "")
        user_query, strategy = _prompt_for_query(tool_name, tool_desc, strategy, llm)

        # Invoke the agent, show its response (or error), let the user decide to retry
        success = False
        while True:
            # use a fresh thread-id so previous messages aren't reused
            cfg = {"configurable": {"thread_id": str(uuid4())}}
            print("Invoking agent, please wait …")
            exc: Exception | None = None
            try:
                await agent.ainvoke({"messages": [{"role": "user", "content": user_query}]}, cfg)
            except Exception as e:  # capture, but don't abort
                exc = e

            if exc:
                print(f"\nInvocation raised an error:\n{exc}\n")
            else:
                # Show LLM/agent final response
                state = agent.get_state(cfg)
                output_msg = state.values.get("messages", [])[-1]
                output_content = getattr(output_msg, "content", str(output_msg))
                print("\nLLM response:\n")
                print(output_content)
                success = True

            choice = input(
                "Retry with different query (r) or continue to the next tool (enter)? "
            ).strip().lower()
            if choice == "r":
                user_query, strategy = _prompt_for_query(tool_name, tool_desc, strategy, llm)
                continue
            break

        if success:
            trajectory = extract_langgraph_trajectory_from_thread(agent, cfg)
            if replace_existing:
                for i in reversed(existing_idx):  # pop from the end to keep indices valid
                    dataset.pop(i)
            dataset.append({
                "tool": tool_name,
                "input": user_query,
                "output": output_content,
                "trajectory": trajectory,
            })
            dataset_path.write_text(yaml.safe_dump({"tests": dataset}))
            print(f"Recorded trace for '{tool_name}'.\n")
            completed_tools.add(tool_name)
            if tool_name in remaining_tools:
                remaining_tools.remove(tool_name)

    print("Evaluation session finished.")


def main() -> None:  # pragma: no cover
    asyncio.run(_interactive_eval())


if __name__ == "__main__":  # pragma: no cover
    main()
