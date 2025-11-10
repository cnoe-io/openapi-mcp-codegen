# Copyright 2025 CNOE
"""Launch an A2A HTTP server exposing the Argo_rollouts agent."""

from cnoe_agent_utils.tracing import disable_a2a_tracing

disable_a2a_tracing()  # Or import automatically disables A2A

import os
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
from starlette.middleware.cors import CORSMiddleware

from .agent_executor import Argo_rolloutsAgentExecutor

load_dotenv()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_agent_card(host: str, port: int) -> AgentCard:
  """Return AgentCard with skills from config or fallback."""
  capabilities = AgentCapabilities(streaming=True, push_notifications=True)

  # Define skills from config or fallback to generated single skill

  # Skills from config.yaml
  skills = [
    AgentSkill(
      id="rollout_management",
      name="Rollout Management",
      description="Core rollout operations for creating, managing, and monitoring Argo Rollouts",
      tags=["rollouts", "deployments", "lifecycle", "management"],
      examples=[
        "List all rollouts in the default namespace",
        "Get the status and details of rollout 'web-app'",
        "Create a new rollout with canary deployment strategy",
        "Delete rollout 'old-service' from namespace 'production'",
        "Promote rollout 'api-service' to the next step",
        "Abort rollout 'failed-deployment' and revert to stable",
        "Pause rollout 'frontend-app' during deployment",
        "Resume paused rollout 'backend-service'",
        "Restart rollout 'data-api' to trigger new deployment",
        "Scale rollout 'worker-service' to 5 replicas",
      ],
    ),
    AgentSkill(
      id="analysis_templates",
      name="Analysis Templates",
      description="Manage analysis templates for automated rollout validation and testing",
      tags=["analysis", "templates", "validation", "testing"],
      examples=[
        "List all analysis templates in the 'monitoring' namespace",
        "Create a new analysis template for success rate validation",
        "Get details of analysis template 'error-rate-check'",
        "Update analysis template 'latency-test' with new metrics",
        "Delete unused analysis template 'legacy-validation'",
        "Configure analysis template for Prometheus metrics",
        "Set up analysis template for custom application metrics",
      ],
    ),
    AgentSkill(
      id="analysis_runs",
      name="Analysis Runs",
      description="Monitor and manage analysis runs for rollout validation",
      tags=["analysis", "runs", "monitoring", "validation"],
      examples=[
        "List all analysis runs for rollout 'web-frontend'",
        "Get details of analysis run 'performance-test-123'",
        "Monitor analysis run status for deployment validation",
        "Get analysis run results and metrics",
        "List failed analysis runs in the last 24 hours",
        "Get analysis run logs for troubleshooting",
      ],
    ),
    AgentSkill(
      id="experiments",
      name="Experiments",
      description="Manage A/B testing and experimentation using Argo Rollouts",
      tags=["experiments", "a-b-testing", "traffic-splitting", "testing"],
      examples=[
        "List all experiments in the 'experiments' namespace",
        "Create a new A/B test experiment for feature flag",
        "Get experiment details and traffic split configuration",
        "Update experiment 'checkout-flow-test' with new weights",
        "Delete completed experiment 'button-color-test'",
        "Monitor experiment metrics and success criteria",
        "Get experiment results and statistical analysis",
      ],
    ),
    AgentSkill(
      id="cluster_analysis_templates",
      name="Cluster Analysis Templates",
      description="Manage cluster-wide analysis templates available across all namespaces",
      tags=["cluster-templates", "global", "analysis", "shared-resources"],
      examples=[
        "List all cluster analysis templates",
        "Create a cluster-wide template for common validation patterns",
        "Get details of cluster template 'global-health-check'",
        "Update cluster template 'security-scan' with new rules",
        "Delete unused cluster template 'deprecated-validation'",
        "Configure cluster template for organization-wide metrics",
      ],
    ),
    AgentSkill(
      id="monitoring_observability",
      name="Monitoring & Observability",
      description="Access logs, metrics, and monitoring data for rollouts and deployments",
      tags=["logs", "metrics", "monitoring", "debugging", "observability"],
      examples=[
        "Get rollout deployment history and events",
        "View rollout replica set status and progression",
        "Monitor rollout canary analysis results",
        "Get rollout logs and pod information",
        "Track rollout promotion steps and timing",
        "View rollout traffic routing and weights",
        "Monitor rollout health checks and readiness",
        "Get rollout error events and troubleshooting info",
      ],
    ),
    AgentSkill(
      id="system_information",
      name="System Information",
      description="Access Argo Rollouts controller information and system status",
      tags=["system", "info", "version", "status", "health"],
      examples=[
        "Get Argo Rollouts controller version and build information",
        "Check Argo Rollouts system health and component status",
        "Get controller configuration and feature flags",
        "View Argo Rollouts resource usage and performance metrics",
        "Get API server capabilities and supported features",
        "Check controller permissions and RBAC status",
      ],
    ),
  ]

  return AgentCard(
    name="Argo_rollouts Agent",
    description="Auto-generated A2A wrapper for Argo_rollouts MCP server.",
    url=f"http://{host}:{port}/",
    version="0.1.0",
    defaultInputModes=["text/plain"],
    defaultOutputModes=["text/plain"],
    capabilities=capabilities,
    skills=skills,
  )


def _build_server(host: str, port: int):
  httpx_client = httpx.AsyncClient()
  push_config_store = InMemoryPushNotificationConfigStore()
  push_sender = BasePushNotificationSender(
    httpx_client=httpx_client,
    config_store=push_config_store,
  )
  request_handler = DefaultRequestHandler(
    agent_executor=Argo_rolloutsAgentExecutor(),
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
  app = server.build()

  # Add CORS middleware to allow cross-origin requests
  cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
  cors_methods = os.getenv("CORS_METHODS", "*").split(",") if os.getenv("CORS_METHODS") != "*" else ["*"]
  cors_headers = os.getenv("CORS_HEADERS", "*").split(",") if os.getenv("CORS_HEADERS") != "*" else ["*"]

  app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Configurable origins
    allow_methods=cors_methods,  # Configurable HTTP methods
    allow_headers=cors_headers,  # Configurable headers
    allow_credentials=os.getenv("CORS_CREDENTIALS", "false").lower() == "true",
  )

  uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
  main()
