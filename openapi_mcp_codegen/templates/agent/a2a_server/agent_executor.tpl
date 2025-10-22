{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""AgentExecutor implementation that connects the {{ mcp_name | capitalize }} agent to A2A.

  Extends BaseAgentExecutor to provide {{ mcp_name }}-specific agent execution.
  Streams intermediate status updates while tools run and emits a final artifact
  when the agent completes.
  """

import logging
from typing_extensions import override

from cnoe_agent_utils.tracing import disable_a2a_tracing
disable_a2a_tracing()  # Disable A2A internal tracing

from a2a.server.agent_execution import RequestContext
from a2a.server.events import EventQueue

from .base_agent_executor import BaseAgentExecutor
from .agent import {{ mcp_name | capitalize }}Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {{ mcp_name | capitalize }}AgentExecutor(BaseAgentExecutor):
    """Executes tasks using the {{ mcp_name | capitalize }} agent with streaming support."""

    def __init__(self) -> None:
        """Initialize the executor with the {{ mcp_name }} agent."""
        agent = {{ mcp_name | capitalize }}Agent()
        super().__init__(agent)
