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

from dotenv import load_dotenv

from rich import print as rprint, box
from langfuse import get_client

load_dotenv()

logger = logging.getLogger(__name__)

class SkipTool(Exception):
    """Raised when the evaluator decides to skip the current tool."""

class QuitEvaluation(Exception):
    """Raised when the evaluator decides to quit the session."""

def _in(prompt: str) -> str:
    """Input wrapper that raises SkipTool on (s|skip) and QuitEvaluation on (q|quit)."""
    val = input(prompt).strip()
    if val.lower() in ("s", "skip"):
        raise SkipTool
    if val.lower() in ("q", "quit"):
        raise QuitEvaluation
    return val


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
        rprint(f"[bold magenta]\\nDescription:[/] {tool_desc}")
    rprint(f"[bold yellow]Using strategy:[/] '{strategy or 'None'}'")

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
            rprint(f"[cyan]Suggested query:[/] {suggested_query}")

        try:
            inp = _in(
                "Enter a user query "
                "(press Enter to accept suggestion, (u)pdate strategy, (s)kip or (q)uit): "
            )
        except SkipTool:
            raise
        except QuitEvaluation:
            raise

        if inp.lower() in ("u", "update"):
            strategy = _in("Enter new evaluation strategy (or (s)kip/(q)uit): ")
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
    try:
        strategy = _in(
            "Optional global evaluation strategy "
            "(e.g. resource names) – press Enter, (s)kip or (q)uit: "
        )
    except SkipTool:
        strategy = ""
    except QuitEvaluation:
        print("Exiting evaluation session.")
        return

    # Create one LLM instance for all query suggestions
    llm = None
    try:
        llm = LLMFactory().get_llm()
    except Exception as e:
        logger.warning("LLM init failed: %s", e)

    # ----------------------------------------------------- helper
    def _mark_skipped(tn: str) -> None:
        """Ensure exactly one {'tool': <tn>} entry exists for a skipped tool."""
        # Find all existing *skipped* entries for this tool (len == 1 → skipped)
        skip_idxs = [
            i for i, t in enumerate(dataset)
            if t.get("tool") == tn and len(t) == 1
        ]

        if skip_idxs:
            # Keep the first, remove any further duplicates
            for i in reversed(skip_idxs[1:]):
                dataset.pop(i)
        else:
            # Only add a new skipped stub if none exists yet
            dataset.append({"tool": tn})

        # Persist + update bookkeeping
        dataset_path.write_text(yaml.safe_dump({"tests": dataset}))
        skipped_tools.add(tn)
        if tn in remaining_tools:
            remaining_tools.remove(tn)

    try:
        get_client().update_current_trace(tags=["{{ mcp_name }}-eval-mode"])
    except Exception:
        pass
    agent, tools = await create_agent()
    tool_map = {t.name: t for t in tools}
    all_tools = [t.name for t in tools]                          # full list

    completed_tools: set[str] = set()
    skipped_tools: set[str] = set()
    for t in dataset:
        if len(t.keys()) == 1 and "tool" in t:       # only “tool” → skipped entry
            skipped_tools.add(t["tool"])
        else:
            completed_tools.add(t["tool"])

    remaining_tools = [t for t in all_tools if t not in completed_tools and t not in skipped_tools]

    try:
        while True:
            rprint("\n[bold green]Tools:[/]")
            for idx, tool in enumerate(all_tools, start=1):
                if tool in skipped_tools:
                    marker = "[red](skipped)[/]"
                elif tool in completed_tools:
                    marker = "[green](done)[/]"
                else:
                    marker = ""
                rprint(f"{idx}. {tool} {marker}")
            # Prompt user – default is the next tool in the list
            default_tool = remaining_tools[0] if remaining_tools else all_tools[0]
            try:
                choice = _in(
                    f"Select tool to evaluate [{default_tool}] "
                    "(enter/number/(s)kip/(q)uit): "
                )
            except SkipTool:
                _mark_skipped(default_tool)
                continue
            except QuitEvaluation:
                raise

            if choice == "":
                tool_name = default_tool
            elif choice.lower() in ("s", "skip"):
                _mark_skipped(default_tool)
                continue
            elif choice.isdigit():
                idx = int(choice) - 1
                if not (0 <= idx < len(all_tools)):
                    rprint("[red]Invalid number, try again.[/]")
                    continue
                tool_name = all_tools[idx]
            else:
                rprint("[red]Invalid input, enter a number, press Enter for default, or 's' to skip.[/]")
                continue

            # ------------------------------------------------- dataset clash check
            existing_idx: list[int] = [
                i for i, t in enumerate(dataset) if t.get("tool") == tool_name
            ]
            replace_existing = False
            if existing_idx:
                try:
                    choice = _in(
                        f"{len(existing_idx)} existing test(s) for '{tool_name}' found – "
                        "(r)eplace, (a)dd as extra, (s)kip or (q)uit? [a]: "
                    ).lower()
                    replace_existing = choice == "r"
                except SkipTool:
                    rprint("[yellow]Skipped.[/]\n")
                    _mark_skipped(tool_name)
                    continue
                except QuitEvaluation:
                    raise

            tool_desc = getattr(tool_map[tool_name], "description", "")
            try:
                user_query, strategy = _prompt_for_query(tool_name, tool_desc, strategy, llm)
            except SkipTool:
                rprint("[yellow]Skipped.[/]\n")
                _mark_skipped(tool_name)
                continue
            except QuitEvaluation:
                raise

            # Invoke the agent, show its response (or error), let the user decide to retry
            success = False
            while True:
                # use a fresh thread-id so previous messages aren't reused
                cfg = {"configurable": {"thread_id": str(uuid4())}}
                rprint("[blue]Invoking agent, please wait …[/]")
                exc: Exception | None = None
                try:
                    await agent.ainvoke({"messages": [{"role": "user", "content": user_query}]}, cfg)
                except Exception as e:  # capture, but don't abort
                    exc = e

                if exc:
                    rprint(f"\n[red]Invocation raised an error:[/]\n{exc}\n")
                else:
                    # Show LLM/agent final response
                    state = agent.get_state(cfg)
                    output_msg = state.values.get("messages", [])[-1]
                    output_content = getattr(output_msg, "content", str(output_msg))
                    rprint("\n[bold green]LLM response:[/]\n")
                    rprint(output_content)
                    success = True

                try:
                    choice = _in(
                        "Retry with different query (r), continue (enter), (s)kip or (q)uit: "
                    ).lower()
                except SkipTool:
                    rprint("[yellow]Skipped.[/]\n")
                    _mark_skipped(tool_name)
                    success = False
                    break          # exit retry loop, proceed to next tool
                except QuitEvaluation:
                    raise
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
                rprint(f"[green]Recorded trace for '{tool_name}'.[/]\n")
                completed_tools.add(tool_name)
                skipped_tools.discard(tool_name)
                if tool_name in remaining_tools:
                    remaining_tools.remove(tool_name)

    except QuitEvaluation:
        print("Exiting evaluation session.")
        return

    rprint("[bold green]Evaluation session finished.[/]")


def main() -> None:  # pragma: no cover
    asyncio.run(_interactive_eval())


if __name__ == "__main__":  # pragma: no cover
    main()
