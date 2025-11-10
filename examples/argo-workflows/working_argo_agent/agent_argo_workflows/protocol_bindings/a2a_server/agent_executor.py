# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

from .agent import ArgoWorkflowsAgent
from .base_langgraph_agent_executor import BaseLangGraphAgentExecutor


class ArgoWorkflowsAgentExecutor(BaseLangGraphAgentExecutor):
    """Argo Workflows AgentExecutor using base class."""

    def __init__(self):
        super().__init__(ArgoWorkflowsAgent())