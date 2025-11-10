{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""AgentExecutor implementation that connects the {{ mcp_name | capitalize }} agent to A2A.

This class inherits from BaseLangGraphAgentExecutor to leverage common A2A protocol
handling, streaming support, and error management while providing {{ mcp_name }}-specific
agent initialization.
"""

import logging
from typing_extensions import override

from cnoe_agent_utils.tracing import disable_a2a_tracing
disable_a2a_tracing()  # Disable A2A tracing to prevent conflicts

from cnoe_agent_utils.agents import BaseLangGraphAgentExecutor
from .agent import {{ mcp_name | capitalize }}Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {{ mcp_name | capitalize }}AgentExecutor(BaseLangGraphAgentExecutor):
    """
    Executes tasks using the {{ mcp_name | capitalize }} LangGraph agent.

    Inherits comprehensive A2A protocol handling, streaming support, task state
    management, and error handling from BaseLangGraphAgentExecutor.
    """

    def __init__(self) -> None:
        """Initialize with {{ mcp_name | capitalize }}Agent instance."""
        # Initialize the base class with our specific agent
        super().__init__(agent={{ mcp_name | capitalize }}Agent())
        logger.info("Initialized {{ mcp_name | capitalize }}AgentExecutor")

    @override
    def _validate_request(self, context) -> bool:
        """
        Validate the incoming request context.

        Override this method to add {{ mcp_name }}-specific validation logic.
        Return True if validation fails, False if request is valid.
        """
        # Add any {{ mcp_name }}-specific validation here
        # For now, accept all requests
        return False

    # Note: execute() and cancel() methods are inherited from BaseLangGraphAgentExecutor
    # which provides:
    # - Full streaming support with task state transitions
    # - Comprehensive error handling and logging
    # - Proper A2A protocol compliance
    # - Artifact management
    # - Context and trace management
