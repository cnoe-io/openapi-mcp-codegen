{{ file_header }}

"""
{{ agent_display_name }} Agent using BaseLangGraphAgent.

This agent connects to an external MCP server at {{ mcp_server_url }}.
It provides consistent behavior with other A2A agents.
"""

import logging
import os
from typing import Dict, Any, Literal
from dotenv import load_dotenv
from pydantic import BaseModel

from agent_{{ agent_name }}.utils.base_agent import BaseLangGraphAgent
from agent_{{ agent_name }}.utils.prompt_templates import scope_limited_agent_instruction

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""
    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


class {{ agent_display_name.replace(' ', '') }}Agent(BaseLangGraphAgent):
    """{{ agent_display_name }} Agent using BaseLangGraphAgent for consistent streaming."""

    {% if system_prompt %}
    SYSTEM_INSTRUCTION = """{{ system_prompt }}"""
    {% else %}
    SYSTEM_INSTRUCTION = scope_limited_agent_instruction(
        service_name="{{ agent_display_name }}",
        service_operations="interact with {{ agent_display_name }} API through MCP server",
        additional_guidelines=[
            "Before executing any tool, ensure that all required parameters are provided",
            "If any required parameters are missing, ask the user to provide them",
            "Always use the most appropriate tool for the requested operation and validate parameters",
            "When working with API operations, use clear and descriptive responses",
            "The MCP server provides access to {{ agent_display_name }} functionality - use the available tools appropriately"
        ],
        include_error_handling=True,  # Real API calls through MCP server
        include_date_handling=True    # Enable date handling
    )
    {% endif %}

    RESPONSE_FORMAT_INSTRUCTION = (
        'Select status as completed if the request is complete. '
        'Select status as input_required if the input is a question to the user. '
        'Set response status to error if the input indicates an error.'
    )

    def __init__(self):
        """Initialize {{ agent_display_name }} agent with MCP server connection."""
        self.mcp_server_url = "{{ mcp_server_url }}"

        if not self.mcp_server_url:
            logger.warning("MCP server URL not configured properly")

        # Call parent constructor (no parameters needed)
        super().__init__()

    def get_agent_name(self) -> str:
        """Return the agent name."""
        return "{{ agent_name }}"

    def get_mcp_http_config(self) -> Dict[str, Any] | None:
        """
        Provide HTTP MCP configuration for {{ agent_display_name }} API access.

        Returns:
            Dictionary with {{ agent_display_name }} MCP server configuration
        """
        if not self.mcp_server_url:
            logger.error("Cannot configure MCP: Server URL not set")
            return None

        return {
            "url": self.mcp_server_url,
            "headers": {
                "Content-Type": "application/json",
            },
        }

    def get_mcp_config(self, server_path: str | None = None) -> Dict[str, Any]:
        """
        Not used for {{ agent_display_name }} agent (HTTP mode only).

        This method is required by the base class but not used since we
        override get_mcp_http_config() for HTTP-only operation.
        """
        raise NotImplementedError(
            "{{ agent_display_name }} agent uses HTTP mode only. "
            "Use get_mcp_http_config() instead."
        )

    def get_system_instruction(self) -> str:
        """Return the system instruction for the agent."""
        return self.SYSTEM_INSTRUCTION

    def get_response_format_class(self):
        """Return the response format class."""
        return ResponseFormat

    def get_response_format_instruction(self) -> str:
        """Return the response format instruction."""
        return self.RESPONSE_FORMAT_INSTRUCTION

    def get_tool_working_message(self) -> str:
        """Return the message shown when a tool is being invoked."""
        return "🔧 Calling tool: **{tool_name}**"

    def get_tool_processing_message(self) -> str:
        """Return the message shown when processing tool results."""
        return "✅ Tool **{tool_name}** completed"
