{{ file_header }}

"""
Base agent class for A2A agents.
Remote agent pattern - connects to external MCP server via HTTP.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseLangGraphAgent(ABC):
    """
    Base class for remote A2A agents that connect to external MCP servers.

    This follows the GitHub agent pattern:
    Agent Chat CLI → A2A Agent → MCP Server (AgentGateway) → Target API

    The agent receives tool calls via A2A protocol and processes them using
    the MCP server connection configured in the agent.
    """

    def __init__(self):
        """Initialize the base agent."""
        logger.info(f"Initializing {self.get_agent_name()} agent")

    @abstractmethod
    def get_agent_name(self) -> str:
        """Return the agent name."""
        pass

    @abstractmethod
    def get_mcp_http_config(self) -> Optional[Dict[str, Any]]:
        """
        Return MCP HTTP configuration for the remote server.

        Returns:
            Dict with MCP server URL and headers, or None if not configured
        """
        pass

    @abstractmethod
    def get_system_instruction(self) -> str:
        """Return the system instruction for the agent."""
        pass

    @abstractmethod
    def get_response_format_class(self):
        """Return the response format class."""
        pass

    @abstractmethod
    def get_response_format_instruction(self) -> str:
        """Return the response format instruction."""
        pass

    def get_tool_working_message(self) -> str:
        """Return the message shown when a tool is being invoked."""
        return "🔧 Working on: **{tool_name}**"

    def get_tool_processing_message(self) -> str:
        """Return the message shown when processing tool results."""
        return "✅ Completed: **{tool_name}**"

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with input data.

        For remote agents, this method should:
        1. Process the user input
        2. Determine what actions are needed
        3. Return appropriate response

        Tool execution happens via the MCP server integration at the
        A2A framework level, not within this agent class.
        """
        try:
            message = input_data.get("message", "")
            logger.info(f"Processing message: {message[:100]}...")

            # Basic response - actual implementation would be more sophisticated
            response = {
                "status": "completed",
                "message": f"I can help you with {self.get_agent_name()} operations. "
                          f"Please specify what you'd like to do: {message}"
            }

            return response
        except Exception as e:
            logger.error(f"Agent invocation failed: {e}")
            return {
                "status": "error",
                "message": f"Error processing request: {str(e)}"
            }
