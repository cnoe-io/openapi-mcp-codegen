{{ file_header }}

from dotenv import load_dotenv

from a2a.types import (
  AgentCapabilities,
  AgentCard,
  AgentSkill
)

load_dotenv()

# ==================================================
# AGENT SPECIFIC CONFIGURATION
# Modify these values for your specific agent
# ==================================================
AGENT_NAME = '{{ agent_name }}'
AGENT_DESCRIPTION="{{ agent_description }}"

# Define agent skills from config or fallback to generated single skill
{% if skills %}
# Skills from config.yaml
agent_skills = [
{% for skill in skills %}
    AgentSkill(
        id="{{ skill.id }}",
        name="{{ skill.name }}",
        description="{{ skill.description }}",
        tags={{ skill.tags | list }},
        examples=[
{% for example in skill.examples %}
            "{{ example }}",
{% endfor %}
        ]
    ),
{% endfor %}
]
{% else %}
# Fallback single skill from OpenAPI spec
agent_skills = [
    AgentSkill(
        id="{{ agent_name }}_agent_skill",
        name="{{ agent_display_name }} Agent Skill",
        description="Handles tasks related to {{ agent_display_name }} operations via MCP server.",
        tags=[
            "{{ agent_name }}",
            "mcp",
            "api management",
            "automation"
        ],
        examples=[
{% for example in skill_examples %}
            {{ example }},
{% endfor %}
        ]
    )
]
{% endif %}

# ==================================================
# SHARED CONFIGURATION - DO NOT MODIFY
# This section is reusable across all agents
# ==================================================
SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

capabilities = AgentCapabilities(streaming=True, pushNotifications=True)

def create_agent_card(agent_url):
  print("===================================")
  print(f"       {AGENT_NAME.upper()} AGENT CONFIG      ")
  print("===================================")
  print(f"AGENT_URL: {agent_url}")
  print(f"MCP_SERVER_URL: {{ mcp_server_url }}")
  print("===================================")

  return AgentCard(
    name=AGENT_NAME,
    id=f'{AGENT_NAME.lower()}-tools-agent',
    description=AGENT_DESCRIPTION,
    url=agent_url,
    version='0.1.0',
    defaultInputModes=SUPPORTED_CONTENT_TYPES,
    defaultOutputModes=SUPPORTED_CONTENT_TYPES,
    capabilities=capabilities,
    skills=agent_skills,
    # Using the security field instead of the non-existent AgentAuthentication class
    security=[{"public": []}],
  )
