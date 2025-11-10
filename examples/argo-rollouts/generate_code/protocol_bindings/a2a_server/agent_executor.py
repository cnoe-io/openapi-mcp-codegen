# Copyright 2025 CNOE
"""AgentExecutor implementation that connects the Argo_rollouts agent to A2A.

This class inherits from BaseLangGraphAgentExecutor to leverage common A2A protocol
handling, streaming support, and error management while providing argo_rollouts-specific
agent initialization.
"""

import logging
from typing_extensions import override

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Disable A2A tracing to prevent conflicts

from cnoe_agent_utils.agents import BaseLangGraphAgentExecutor
from .agent import Argo_rolloutsAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Argo_rolloutsAgentExecutor(BaseLangGraphAgentExecutor):
  """
  Executes tasks using the Argo_rollouts LangGraph agent.

  Inherits comprehensive A2A protocol handling, streaming support, task state
  management, and error handling from BaseLangGraphAgentExecutor.
  """

  def __init__(self) -> None:
    """Initialize with Argo_rolloutsAgent instance."""
    # Initialize the base class with our specific agent
    super().__init__(agent=Argo_rolloutsAgent())
    logger.info("Initialized Argo_rolloutsAgentExecutor")

  @override
  def _validate_request(self, context) -> bool:
    """
    Validate the incoming request context.

    Override this method to add argo_rollouts-specific validation logic.
    Return True if validation fails, False if request is valid.
    """
    # Add any argo_rollouts-specific validation here
    # For now, accept all requests
    return False

  # Note: execute() and cancel() methods are inherited from BaseLangGraphAgentExecutor
  # which provides:
  # - Full streaming support with task state transitions
  # - Comprehensive error handling and logging
  # - Proper A2A protocol compliance
  # - Artifact management
  # - Context and trace management
