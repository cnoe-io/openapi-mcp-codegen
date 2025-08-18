{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""{{ mcp_name | capitalize }} LangGraph agent wrapper used by the A2A server.

  This class adapts the LangGraph agent to the A2A streaming protocol by emitting
  generic status updates during tool use and a final completion message.
  """

import asyncio
import logging
import os
from typing import AsyncIterable, Any, Dict
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.callbacks import BaseCallbackHandler
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from .state import AgentState, InputState, Message, MsgType
from cnoe_agent_utils import LLMFactory
from langfuse import get_client
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

logger = logging.getLogger(__name__)
memory = MemorySaver()


async def _bootstrap_langgraph_agent():
    """Launch the generated MCP server via MultiServerMCPClient and return a LangGraph React agent."""
    load_dotenv()
    token = os.getenv("{{ mcp_name | upper }}_TOKEN")
    api_url = os.getenv("{{ mcp_name | upper }}_API_URL")
    if not token or not api_url:
        raise EnvironmentError("Both {{ mcp_name | upper }}_API_URL and {{ mcp_name | upper }}_TOKEN must be set")

    from agent import create_agent  # noqa: E402
    agent, _ = await create_agent()
    try:
        get_client().update_current_trace(tags=["{{ mcp_name }}-a2a"])
    except Exception:
        pass
    return agent


class {{ mcp_name | capitalize }}Agent:
    """A thin streaming wrapper that adapts the LangGraph agent to the A2A protocol."""

    async def stream(
        self,
        query: str,
        session_id: str,
        callbacks: list[BaseCallbackHandler] | None = None,
    ) -> AsyncIterable[Dict[str, Any]]:
        agent = await _bootstrap_langgraph_agent()
        cfg: RunnableConfig = {"configurable": {"thread_id": session_id}}

        lf = get_client()
        lf_handler = None
        try:
            lf_handler = LangfuseCallbackHandler()
        except Exception:
            pass

        async def _async_gen():
            with lf.start_as_current_span(
                name="{{ mcp_name }}-query",
                input={"query": query, "session_id": session_id},
            ) as root_span:
                # Tag the trace and set session id
                root_span.update_trace(tags=["{{ mcp_name }}-a2a"], session_id=session_id)
                async for item in agent.astream(
                    {"messages": [("user", query)]},
                    {**cfg, "callbacks": ([lf_handler] if lf_handler else [])},
                    stream_mode="values",
                ):
                    yield item
                state = agent.get_state(cfg)
                output_msg = state.values.get("messages", [])[-1]
                root_span.update_trace(output={"response": getattr(output_msg, "content", str(output_msg))})

        agen = _async_gen()

        async for item in agen:
            msg = item["messages"][-1]
            if isinstance(msg, AIMessage) and msg.tool_calls:
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Looking up required data via tools...",
                }
            elif isinstance(msg, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Processing tool output...",
                }

        # Final response or input-required guard
        state = agent.get_state(cfg)
        output_msg = state.values.get("messages", [])[-1]

        # If the final assistant message asks for clarification, request user input
        final_text = getattr(output_msg, "content", str(output_msg)) or ""
        if isinstance(output_msg, AIMessage) and any(
            kw in final_text.lower() for kw in ["please provide", "need more info", "could you clarify"]
        ):
            yield {
                "is_task_complete": False,
                "require_user_input": True,
                "content": final_text,
            }
            return
        yield {
            "is_task_complete": True,
            "require_user_input": False,
            "content": getattr(output_msg, "content", str(output_msg)),
        }
