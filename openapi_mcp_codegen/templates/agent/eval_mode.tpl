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
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

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

    # ----------------------------------------------------------- allow alternate dataset
    try:
        alt_path = _in("Use alternate dataset file? Enter path or press Enter for default (eval/dataset.yaml): ")
    except SkipTool:
        alt_path = ""
    except QuitEvaluation:
        print("Exiting evaluation session.")
        return

    if alt_path:
        dataset_path = Path(alt_path).expanduser().resolve()
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

    # -------- initial tools status summary
    rprint("\n[bold green]Current tool status:[/]")
    for t in all_tools:
        if t in skipped_tools:
            marker = "[red](skipped)[/]"
        elif t in completed_tools:
            marker = "[green](done)[/]"
        else:
            marker = "[yellow](pending)[/]"
        rprint(f"- {t} {marker}")

    # ---------------------------------------------------------------- helper: extract combined LLM + tool output
    def _extract_combined_output(agent, cfg) -> str:
        state = agent.get_state(cfg)
        output_msg = state.values.get("messages", [])[-1]
        output_content = getattr(output_msg, "content", str(output_msg))
        messages = state.values.get("messages", [])
        tool_outputs: list[str] = []
        for m in messages:
            try:
                m_type = getattr(m, "type", None) or getattr(m, "role", None)
                if str(m_type).lower() == "tool" or m.__class__.__name__ == "ToolMessage":
                    content = getattr(m, "content", None)
                    if isinstance(content, str) and content.strip():
                        tool_outputs.append(content.strip())
            except Exception:
                continue
        if tool_outputs:
            return output_content + "\n\n" + "\n\n".join(tool_outputs)
        return output_content

    # ---------------------------------------------------------------- helper: parallel re-run of all existing items
    async def _rerun_all_existing(agent, dataset: list[dict], dest_path: Path) -> None:
        # Collect indices of runnable items (those with input/trajectory/output)
        runnable = [
            (i, it)
            for i, it in enumerate(dataset)
            if {"tool", "input", "trajectory", "output"} <= set(it.keys())
        ]
        if not runnable:
            rprint("[yellow]No existing completed items to re-run.[/]")
            return

        rprint(f"[cyan]Re-running {len(runnable)} existing items in parallel...[/]")

        async def _process(idx: int, item: dict):
            cfg = {"configurable": {"thread_id": str(uuid4())}}
            try:
                await agent.ainvoke({"messages": [{"role": "user", "content": item["input"]}]}, cfg)
            except Exception as e:  # noqa: BLE001
                return idx, {"error": str(e)}
            new_traj = extract_langgraph_trajectory_from_thread(agent, cfg)
            combined_output = _extract_combined_output(agent, cfg)
            return idx, {
                "tool": item["tool"],
                "input": item["input"],
                "output": combined_output,
                "trajectory": new_traj,
            }

        tasks = [_process(i, it) for i, it in runnable]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Apply updates back into dataset preserving order
        updated_count = 0
        for res in results:
            if isinstance(res, Exception):
                continue
            idx, new_item = res
            if isinstance(new_item, dict) and "error" not in new_item:
                dataset[idx] = new_item
                updated_count += 1

        # Persist updated dataset
        dest_path.write_text(yaml.safe_dump({"tests": dataset}))
        rprint(f"[green]Updated {updated_count} items in dataset.[/]\n")

    # ---------------------------------------------------------------- optional initial rerun
    try:
        rerun_choice = _in("Re-run all existing completed items now? (y/N): ")
    except SkipTool:
        rerun_choice = "n"
    except QuitEvaluation:
        print("Exiting evaluation session.")
        return

    if rerun_choice.lower() in ("y", "yes"):
        # Ask where to write the regenerated dataset
        try:
            out_path_inp = _in(f"Output dataset file for regenerated results [default: {dataset_path}]: ")
        except SkipTool:
            out_path_inp = ""
        except QuitEvaluation:
            print("Exiting evaluation session.")
            return
        rerun_dest = Path(out_path_inp).expanduser().resolve() if out_path_inp else dataset_path
        rerun_dest.parent.mkdir(exist_ok=True, parents=True)
        await _rerun_all_existing(agent, dataset, rerun_dest)

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
                    "(enter/number/(ra)=re-run all/(s)kip/(q)uit): "
                )
            except SkipTool:
                _mark_skipped(default_tool)
                continue
            except QuitEvaluation:
                raise

            if choice.lower() in ("ra", "re-run-all"):
                try:
                    out_path_inp = _in(f"Output dataset file for regenerated results [default: {dataset_path}]: ")
                except SkipTool:
                    out_path_inp = ""
                except QuitEvaluation:
                    raise
                rerun_dest = Path(out_path_inp).expanduser().resolve() if out_path_inp else dataset_path
                rerun_dest.parent.mkdir(exist_ok=True, parents=True)
                await _rerun_all_existing(agent, dataset, rerun_dest)
                continue
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
                langfuse = get_client()
                lf_handler = None
                try:
                    lf_handler = LangfuseCallbackHandler()
                except Exception:
                    pass
                try:
                    with langfuse.start_as_current_span(
                        name="{{ mcp_name }}-eval-invoke",
                        input={"query": user_query, "tool": tool_name},
                    ) as span:
                        span.update_trace(tags=["{{ mcp_name }}-eval"], session_id=cfg["configurable"]["thread_id"])
                        await agent.ainvoke(
                            {"messages": [{"role": "user", "content": user_query}]},
                            {**cfg, "callbacks": ([lf_handler] if lf_handler else [])},
                        )
                except Exception as e:  # capture, but don't abort
                    exc = e

                if exc:
                    rprint(f"\n[red]Invocation raised an error:[/]\n{exc}\n")
                else:
                    # Show LLM/agent final response
                    state = agent.get_state(cfg)
                    output_msg = state.values.get("messages", [])[-1]
                    output_content = getattr(output_msg, "content", str(output_msg))

                    # Collect tool call outputs from the full message history
                    messages = state.values.get("messages", [])
                    tool_outputs: list[str] = []
                    for m in messages:
                        try:
                            m_type = getattr(m, "type", None) or getattr(m, "role", None)
                            if str(m_type).lower() == "tool" or m.__class__.__name__ == "ToolMessage":
                                content = getattr(m, "content", None)
                                if isinstance(content, str) and content.strip():
                                    tool_outputs.append(content.strip())
                        except Exception:
                            continue

                    combined_output = output_content
                    if tool_outputs:
                        combined_output = combined_output + "\n\n" + "\n\n".join(tool_outputs)
                    try:
                        span.update_trace(output={"response": combined_output})  # type: ignore[name-defined]
                    except Exception:
                        pass

                    rprint("\n[bold green]LLM response (including tool outputs):[/]\n")
                    rprint(combined_output)
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
                    "output": combined_output,
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
