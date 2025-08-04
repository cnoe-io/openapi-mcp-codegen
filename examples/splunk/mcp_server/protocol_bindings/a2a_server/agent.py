"""Splunk LangGraph agent wrapper used by the A2A server."""

import logging
import os
from typing import AsyncIterable, Any, Dict

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver


logger = logging.getLogger(__name__)
memory = MemorySaver()


async def _bootstrap_langgraph_agent():
  """Launch the generated MCP server via MultiServerMCPClient and return a LangGraph React agent."""
  token = os.getenv("SPLUNK_TOKEN")
  api_url = os.getenv("SPLUNK_API_URL")
  if not token or not api_url:
    raise EnvironmentError("Both SPLUNK_API_URL and SPLUNK_TOKEN must be set")

  from agent import create_agent  # noqa: E402

  return await create_agent()


class SplunkAgent:
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
