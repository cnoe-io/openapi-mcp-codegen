# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""Base agent class with MCP client integration for A2A functionality."""

import logging
import os
import json
import httpx
from abc import ABC, abstractmethod
from collections.abc import AsyncIterable
from typing import Any, Dict, List

from pydantic import BaseModel


logger = logging.getLogger(__name__)


def debug_print(message: str, banner: bool = True):
    """Print debug messages if ACP_SERVER_DEBUG is enabled."""
    if os.getenv("ACP_SERVER_DEBUG", "false").lower() == "true":
        if banner:
            print("=" * 80)
        print(f"DEBUG: {message}")
        if banner:
            print("=" * 80)


class BaseAgent(ABC):
    """
    Base class for A2A agents with MCP client integration.

    Provides MCP server communication and tool invocation.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._mcp_tools = None
        self._http_client = None

    async def _get_http_client(self):
        """Get or create HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    async def _get_mcp_tools(self) -> List[Dict]:
        """Get available tools from MCP server."""
        if self._mcp_tools is not None:
            return self._mcp_tools

        try:
            mcp_config = self.get_mcp_config("")
            mcp_url = mcp_config.get("url", "http://localhost:3001")

            client = await self._get_http_client()

            # MCP tools/list request
            response = await client.post(
                f"{mcp_url}/tools/list",
                json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    self._mcp_tools = data["result"]["tools"]
                    return self._mcp_tools

        except Exception as e:
            logger.warning(f"Failed to get MCP tools: {e}")

        return []

    async def _invoke_mcp_tool(self, tool_name: str, arguments: Dict) -> str:
        """Invoke a tool on the MCP server."""
        try:
            mcp_config = self.get_mcp_config("")
            mcp_url = mcp_config.get("url", "http://localhost:3001")

            client = await self._get_http_client()

            # MCP tools/call request
            response = await client.post(
                f"{mcp_url}/tools/call",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                if "result" in data and "content" in data["result"]:
                    # Extract text content from MCP response
                    content = data["result"]["content"]
                    if isinstance(content, list) and len(content) > 0:
                        return content[0].get("text", str(data["result"]))
                    return str(data["result"])

        except Exception as e:
            logger.error(f"Failed to invoke MCP tool {tool_name}: {e}")
            return f"Error invoking tool {tool_name}: {str(e)}"

        return f"No response from tool {tool_name}"

    async def _process_query_with_tools(self, query: str) -> str:
        """Process user query using available MCP tools."""
        tools = await self._get_mcp_tools()

        if not tools:
            return "No MCP tools available. Make sure the MCP server is running on the configured host:port."

        # Simple query processing - you can enhance this with better NLP
        query_lower = query.lower()

        # Tool selection logic
        if "tools" in query_lower or "help" in query_lower or "what can you do" in query_lower:
            tool_list = "\n".join([f"- {tool['name']}: {tool.get('description', 'No description')}" for tool in tools])
            return f"Available Argo Workflows tools:\n\n{tool_list}\n\nYou can ask me to use any of these tools!"

        elif "list" in query_lower and "workflow" in query_lower:
            # Try to list workflows
            return await self._invoke_mcp_tool("list_workflows", {})

        elif "create" in query_lower and "workflow" in query_lower:
            # Try to create a workflow - this would need more sophisticated parsing
            return await self._invoke_mcp_tool("create_workflow", {"name": "example-workflow"})

        elif "status" in query_lower or "get" in query_lower:
            # Try to get status - would need workflow name parsing
            return "Please specify which workflow you'd like to check the status of."

        else:
            # Default: show available tools and suggest usage
            tool_names = [tool['name'] for tool in tools]
            return f"I have access to these Argo Workflows tools: {', '.join(tool_names)}. Try asking me to 'list workflows' or 'show me your tools' for more details!"

    @abstractmethod
    def get_agent_name(self) -> str:
        """Return the agent's name."""
        pass

    @abstractmethod
    def get_system_instruction(self) -> str:
        """Return the system instruction for the agent."""
        pass

    @abstractmethod
    def get_response_format_instruction(self) -> str:
        """Return the response format instruction."""
        pass

    @abstractmethod
    def get_response_format_class(self) -> type[BaseModel]:
        """Return the response format class."""
        pass

    @abstractmethod
    def get_mcp_config(self, server_path: str) -> dict:
        """Return MCP configuration."""
        pass

    @abstractmethod
    def get_tool_working_message(self) -> str:
        """Return message shown when calling tools."""
        pass

    @abstractmethod
    def get_tool_processing_message(self) -> str:
        """Return message shown when processing tool results."""
        pass

    async def stream(self, query: str, sessionId: str, trace_id: str = None) -> AsyncIterable[Dict[str, Any]]:
        """
        Stream implementation that communicates with MCP server.

        Yields events with:
        - is_task_complete: bool
        - require_user_input: bool
        - content: str
        """
        try:
            # First yield a working message
            yield {
                "is_task_complete": False,
                "require_user_input": False,
                "content": self.get_tool_working_message()
            }

            # Process the query using MCP tools
            response = await self._process_query_with_tools(query)

            # Yield the final response
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": response
            }

        except Exception as e:
            logger.error(f"Error in stream: {e}")
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": f"Sorry, I encountered an error: {str(e)}"
            }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._http_client:
            await self._http_client.aclose()