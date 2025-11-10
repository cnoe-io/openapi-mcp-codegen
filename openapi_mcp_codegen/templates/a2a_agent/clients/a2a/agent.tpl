{{ file_header }}

import os

from agent_{{ agent_name }}.agentcard import (
    create_agent_card,
    agent_skill,
)
from ai_platform_engineering.utils.a2a_common.a2a_remote_agent_connect import (
    A2ARemoteAgentConnectTool,
)

AGENT_HOST = os.getenv("{{ agent_name.upper() }}_AGENT_HOST", "localhost")
AGENT_PORT = os.getenv("{{ agent_name.upper() }}_AGENT_PORT", "8000")
agent_url = f'http://{AGENT_HOST}:{AGENT_PORT}'

agent_card = create_agent_card(agent_url)
tool_map = {
    agent_card.name: agent_skill.examples
}

# initialize the {{ agent_display_name }} agent tool
a2a_remote_agent = A2ARemoteAgentConnectTool(
    name="{{ agent_name }}_tools_agent",
    description=agent_card.description,
    remote_agent_card=agent_card,
    skill_id=agent_skill.id,
)
