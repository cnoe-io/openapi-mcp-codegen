{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""Launch an A2A HTTP server exposing the {{ mcp_name | capitalize }} agent."""

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Or import automatically disables A2A

import asyncio
import os
import click
import uvicorn
import httpx
{% if enable_slim %}from agntcy_app_sdk.factory import AgntcyFactory{% endif %}

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

def _build_server(host: str, port: int):
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
    return A2AStarletteApplication(
        agent_card=_get_agent_card(host, port),
        http_handler=request_handler,
    )

{% if enable_slim %}
async def _run_slim(host: str, port: int) -> None:
    # Run A2A server over SLIM transport (HTTP will run via docker-compose)
    server = _build_server(host, port)
    factory = AgntcyFactory()
    SLIM_ENDPOINT = os.getenv("SLIM_ENDPOINT", "http://localhost:46357")
    transport = factory.create_transport(
        "SLIM",
        endpoint=SLIM_ENDPOINT,
        name=f"default/default/{{ mcp_name }}-agent",
    )
    print("Transport created successfully.")
    bridge = factory.create_bridge(server, transport=transport)
    print("Bridge created successfully. Starting the bridge.")
    await bridge.start(blocking=True)
{% endif %}




@click.command()
@click.option("--host", default="0.0.0.0", help="Bind address")
@click.option("--port", default=10000, help="Port to serve on")
{% if enable_slim %}
@click.option(
    "--enable-slim",
    "slim",
    is_flag=True,
    default=False,
    help="Enable SLIM transport instead of HTTP.",
)
{% endif %}
def main(host: str, port: int{% if enable_slim %}, slim: bool{% endif %}) -> None:
    {% if enable_slim %}
    if slim:
        asyncio.run(_run_slim(host, port))
    else:
        server = _build_server(host, port)
        uvicorn.run(server.build(), host=host, port=port)
    {% else %}
    server = _build_server(host, port)
    uvicorn.run(server.build(), host=host, port=port)
    {% endif %}


if __name__ == "__main__":
    main()
