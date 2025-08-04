{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""LangGraph React-agent wrapper for the generated MCP server."""

import asyncio
import importlib.util
import logging
import os
from pathlib import Path
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from cnoe_agent_utils import LLMFactory

logger = logging.getLogger(__name__)

# Locate the generated MCP server module
spec = importlib.util.find_spec("mcp_{{ mcp_name }}.server")
if not spec or not spec.origin:
    raise ImportError("Cannot find mcp_{{ mcp_name }}.server module")
server_path = str(Path(spec.origin).resolve())


async def create_agent(prompt: str | None = None, response_format=None):
    """
    Spin-up the MCP server as a subprocess via MultiServerMCPClient and build
    a LangGraph React agent that has access to its tools.
    """
    memory = MemorySaver()

    api_url   = os.getenv("{{ mcp_name | upper }}_API_URL")
    api_token = os.getenv("{{ mcp_name | upper }}_TOKEN")
    if not api_url or not api_token:
        raise ValueError("Set {{ mcp_name | upper }}_API_URL and {{ mcp_name | upper }}_TOKEN env vars")

    client = MultiServerMCPClient(
        {
            "{{ mcp_name }}": {
                "command": "uv",
                "args": ["run", server_path],
                "env": {
                    "{{ mcp_name | upper }}_API_URL": api_url,
                    "{{ mcp_name | upper }}_TOKEN": api_token,
                },
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(
        LLMFactory().get_llm(),
        tools=tools,
        checkpointer=memory,
        prompt=prompt,
        response_format=response_format,
    )
    return agent


# Convenience synchronous wrapper
def create_agent_sync(prompt: str | None = None, response_format=None):
    return asyncio.run(create_agent(prompt, response_format))
