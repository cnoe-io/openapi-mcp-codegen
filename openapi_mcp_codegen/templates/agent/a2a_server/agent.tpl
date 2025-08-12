{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""{{ mcp_name | capitalize }} LangGraph agent wrapper used by the A2A server."""

import asyncio
import logging
import os
from typing import AsyncIterable, Any, Dict
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from .state import AgentState, InputState, Message, MsgType
from cnoe_agent_utils import LLMFactory

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
    return agent


class {{ mcp_name | capitalize }}Agent:
    """A thin streaming wrapper that adapts the LangGraph agent to the A2A protocol."""

    async def stream(self, query: str, session_id: str) -> AsyncIterable[Dict[str, Any]]:
        agent = await _bootstrap_langgraph_agent()
        cfg: RunnableConfig = {"configurable": {"thread_id": session_id}}

        async for item in agent.astream({"messages": [("user", query)]}, cfg, stream_mode="values"):
            msg = item["messages"][-1]
            if isinstance(msg, AIMessage) and msg.tool_calls:
                yield {"is_task_complete": False, "require_user_input": False, "content": "Calling tools..."}
            elif isinstance(msg, ToolMessage):
                yield {"is_task_complete": False, "require_user_input": False, "content": "Processing tool output..."}

        # Final response
        state = agent.get_state(cfg)
        output_msg = state.values.get("messages", [])[-1]
        yield {
            "is_task_complete": True,
            "require_user_input": False,
            "content": getattr(output_msg, "content", str(output_msg)),
        }
