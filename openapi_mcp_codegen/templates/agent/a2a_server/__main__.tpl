{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""Launch an A2A HTTP server exposing the {{ mcp_name | capitalize }} agent."""

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Or import automatically disables A2A

import click
import uvicorn
import httpx

from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from .agent_executor import {{ mcp_name | capitalize }}AgentExecutor

load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_agent_card(host: str, port: int) -> AgentCard:
    """Return a minimal AgentCard for the generated agent."""
    capabilities = AgentCapabilities(streaming=True, push_notifications=True)
    skill = AgentSkill(
        id="{{ mcp_name }}",
        name="{{ mcp_name | capitalize }} Tools",
        description="Auto-generated agent exposing {{ mcp_name | capitalize }} MCP tools.",
        tags=["mcp", "{{ mcp_name }}"],
        examples=["Example: call tool X ..."],
    )
    return AgentCard(
        name="{{ mcp_name | capitalize }} Agent",
        description="Auto-generated A2A wrapper for {{ mcp_name | capitalize }} MCP server.",
        url=f"http://{{ '{' }}host{{ '}' }}:{{ '{' }}port{{ '}' }}/",
        version="0.1.0",
        defaultInputModes=["text/plain"],
        defaultOutputModes=["text/plain"],
        capabilities=capabilities,
        skills=[skill],
    )


@click.command()
@click.option("--host", default="0.0.0.0", help="Bind address")
@click.option("--port", default=10000, help="Port to serve on")
def main(host: str, port: int) -> None:
    httpx_client = httpx.AsyncClient()
    push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(
        httpx_client=httpx_client,
        config_store=push_config_store,
    )
    request_handler = DefaultRequestHandler(
        agent_executor={{ mcp_name | capitalize }}AgentExecutor(),
        task_store=InMemoryTaskStore(),
        push_config_store=push_config_store,
        push_sender=push_sender,
    )
    server = A2AStarletteApplication(
        agent_card=_get_agent_card(host, port),
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
