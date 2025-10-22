{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""{{ mcp_name | capitalize }} LangGraph agent wrapper used by the A2A server.

  This class extends BaseAgent to provide {{ mcp_name }}-specific configuration
  and streaming behavior for the A2A protocol.
  """

import logging
import os
import importlib.util
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .base_agent import BaseAgent

load_dotenv()
logger = logging.getLogger(__name__)


# Response format for structured agent output
class {{ mcp_name | capitalize }}ResponseFormat(BaseModel):
    """Structured response format for {{ mcp_name }} agent."""
    status: str = Field(
        description="Status of the task: 'completed', 'input_required', or 'error'"
    )
    message: str = Field(
        description="The response message to the user"
    )


class {{ mcp_name | capitalize }}Agent(BaseAgent):
    """{{ mcp_name | capitalize }} agent implementation extending BaseAgent."""

    def __init__(self):
        """Initialize the {{ mcp_name }} agent."""
        super().__init__()

    def get_agent_name(self) -> str:
        """Return the agent's name."""
        return "{{ mcp_name }}"

    def get_system_instruction(self) -> str:
        """Return the system instruction for the agent."""
        return """You are a helpful assistant that can interact with {{ mcp_name | capitalize }}.

You have access to tools that allow you to:
- Query and retrieve information
- Perform operations
- Manage resources

Always:
1. Use the appropriate tools to fulfill user requests
2. Provide clear, concise responses
3. Ask for clarification when needed
4. Explain what you're doing when using tools

When you complete a task, set status='completed'.
If you need more information from the user, set status='input_required'.
If an error occurs, set status='error'."""

    def get_response_format_instruction(self) -> str:
        """Return the response format instruction."""
        return """Provide your response in the following format:
- status: 'completed' (task done), 'input_required' (need user input), or 'error' (something went wrong)
- message: Your response to the user"""

    def get_response_format_class(self) -> type[BaseModel]:
        """Return the Pydantic response format class."""
        return {{ mcp_name | capitalize }}ResponseFormat

    def get_mcp_config(self, server_path: str) -> Dict[str, Any]:
        """
        Return the MCP server configuration for {{ mcp_name }}.

        Args:
            server_path: Path to the MCP server script

        Returns:
            Dictionary with MCP configuration
        """
        token = os.getenv("{{ mcp_name | upper }}_TOKEN")
        api_url = os.getenv("{{ mcp_name | upper }}_API_URL")

        if not token or not api_url:
            raise EnvironmentError(
                "Both {{ mcp_name | upper }}_API_URL and {{ mcp_name | upper }}_TOKEN must be set"
            )

        return {
            "transport": "stdio",
            "command": "uv",
            "args": ["run", "python", server_path],
            "env": {
                "{{ mcp_name | upper }}_API_URL": api_url,
                "{{ mcp_name | upper }}_TOKEN": token,
            },
        }

    def get_tool_working_message(self) -> str:
        """Return message shown when agent is calling tools."""
        return "Looking up required data via tools..."

    def get_tool_processing_message(self) -> str:
        """Return message shown when agent is processing tool results."""
        return "Processing tool output..."
