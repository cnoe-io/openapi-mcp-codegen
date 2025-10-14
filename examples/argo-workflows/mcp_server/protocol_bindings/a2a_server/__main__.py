# Copyright 2025 CNOE
"""Launch an A2A HTTP server exposing the Argo_workflows agent."""

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

from .agent_executor import Argo_workflowsAgentExecutor

load_dotenv()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_agent_card(host: str, port: int) -> AgentCard:
  """Return a minimal AgentCard for the generated agent."""
  capabilities = AgentCapabilities(streaming=True, push_notifications=True)
  skill = AgentSkill(
    id="argo_workflows",
    name="Argo_workflows Tools",
    description="Auto-generated agent exposing Argo_workflows MCP tools.",
    tags=["mcp", "argo_workflows"],
    examples=["Example: call tool X ..."],
  )
  return AgentCard(
    name="Argo_workflows Agent",
    description="Auto-generated A2A wrapper for Argo_workflows MCP server.",
    url=f"http://{host}:{port}/",
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
    agent_executor=Argo_workflowsAgentExecutor(),
    task_store=InMemoryTaskStore(),
    push_config_store=push_config_store,
    push_sender=push_sender,
  )
  return A2AStarletteApplication(
    agent_card=_get_agent_card(host, port),
    http_handler=request_handler,
  )


@click.command()
@click.option("--host", default="0.0.0.0", help="Bind address")
@click.option("--port", default=10000, help="Port to serve on")
def main(host: str, port: int) -> None:
  server = _build_server(host, port)
  uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
  main()
