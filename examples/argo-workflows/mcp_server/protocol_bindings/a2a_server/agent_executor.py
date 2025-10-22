# Copyright 2025 CNOE
"""AgentExecutor implementation that connects the Argo_workflows agent to A2A.

Extends BaseAgentExecutor to provide argo_workflows-specific agent execution.
Streams intermediate status updates while tools run and emits a final artifact
when the agent completes.
"""

import logging

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Disable A2A internal tracing


from .base_agent_executor import BaseAgentExecutor
from .agent import Argo_workflowsAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Argo_workflowsAgentExecutor(BaseAgentExecutor):
  """Executes tasks using the Argo_workflows agent with streaming support."""

  def __init__(self) -> None:
    """Initialize the executor with the argo_workflows agent."""
    agent = Argo_workflowsAgent()
    super().__init__(agent)
