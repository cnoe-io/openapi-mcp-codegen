# Copyright 2025 CNOE
"""AgentExecutor implementation that connects the Argocd agent to A2A.

This class inherits from BaseLangGraphAgentExecutor to leverage common A2A protocol
handling, streaming support, and error management while providing argocd-specific
agent initialization.
"""

import logging
from typing_extensions import override

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Disable A2A tracing to prevent conflicts

from cnoe_agent_utils.agents import BaseLangGraphAgentExecutor
from .agent import ArgocdAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArgocdAgentExecutor(BaseLangGraphAgentExecutor):
  """
  Executes tasks using the Argocd LangGraph agent.

  Inherits comprehensive A2A protocol handling, streaming support, task state
  management, and error handling from BaseLangGraphAgentExecutor.
  """

  def __init__(self) -> None:
    """Initialize with ArgocdAgent instance."""
    # Initialize the base class with our specific agent
    super().__init__(agent=ArgocdAgent())
    logger.info("Initialized ArgocdAgentExecutor")

  @override
  def _validate_request(self, context) -> bool:
    """
    Validate the incoming request context.

    Override this method to add argocd-specific validation logic.
    Return True if validation fails, False if request is valid.
    """
    # Add any argocd-specific validation here
    # For now, accept all requests
    return False

  # Note: execute() and cancel() methods are inherited from BaseLangGraphAgentExecutor
  # which provides:
  # - Full streaming support with task state transitions
  # - Comprehensive error handling and logging
  # - Proper A2A protocol compliance
  # - Artifact management
  # - Context and trace management
