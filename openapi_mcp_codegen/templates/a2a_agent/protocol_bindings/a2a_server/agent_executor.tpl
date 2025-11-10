{{ file_header }}

"""
{{ agent_display_name }} Agent Executor using BaseLangGraphAgentExecutor.

This provides consistent streaming behavior with other refactored agents
and eliminates duplicate messages.
"""

from agent_{{ agent_name }}.protocol_bindings.a2a_server.agent import {{ agent_display_name.replace(' ', '') }}Agent  # type: ignore[import-untyped]
from agent_{{ agent_name }}.utils.base_agent_executor import BaseLangGraphAgentExecutor


class {{ agent_display_name.replace(' ', '') }}AgentExecutor(BaseLangGraphAgentExecutor):
    """{{ agent_display_name }} AgentExecutor using base class for consistent streaming."""

    def __init__(self):
        super().__init__({{ agent_display_name.replace(' ', '') }}Agent())
