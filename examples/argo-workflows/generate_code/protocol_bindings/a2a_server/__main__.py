# Copyright 2025 CNOE
"""Launch an A2A HTTP server exposing the Argo_workflows agent."""

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

from .agent_executor import Argo_workflowsAgentExecutor

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
      id="workflow_management",
      name="Workflow Management",
      description="Core workflow operations for creating, managing, and monitoring Argo Workflows",
      tags=["workflows", "lifecycle", "management"],
      examples=[
        "List all workflows in the default namespace",
        "Get the status and details of workflow 'my-pipeline'",
        "Create a new workflow from a specification",
        "Delete workflow 'failed-job' from namespace 'production'",
        "Submit a workflow template as a new workflow instance",
        "Lint and validate a workflow specification before creation",
        "Stop a running workflow 'long-running-job'",
        "Suspend workflow 'batch-process' to pause execution",
        "Resume a suspended workflow 'paused-pipeline'",
        "Terminate workflow 'stuck-process' immediately",
        "Set custom parameters or outputs for workflow 'data-pipeline'",
      ],
    ),
    AgentSkill(
      id="workflow_templates",
      name="Workflow Templates",
      description="Manage reusable workflow templates for standardized processes",
      tags=["templates", "reusability", "standardization"],
      examples=[
        "List all workflow templates in the 'ci-cd' namespace",
        "Create a new workflow template for CI/CD pipelines",
        "Get details of workflow template 'build-and-deploy'",
        "Update workflow template 'test-runner' with new steps",
        "Delete obsolete workflow template 'legacy-build'",
        "Lint workflow template before saving changes",
        "Submit workflow template 'data-processing' as a new workflow",
      ],
    ),
    AgentSkill(
      id="cluster_workflow_templates",
      name="Cluster Workflow Templates",
      description="Manage cluster-wide workflow templates available across all namespaces",
      tags=["cluster-templates", "global", "shared-resources"],
      examples=[
        "List all cluster workflow templates",
        "Create a cluster-wide template for common CI/CD patterns",
        "Get details of cluster template 'global-security-scan'",
        "Update cluster template 'compliance-check' with new requirements",
        "Delete unused cluster template 'deprecated-build'",
        "Lint cluster workflow template for validation",
      ],
    ),
    AgentSkill(
      id="cron_workflows",
      name="Scheduled Workflows (Cron)",
      description="Manage recurring and scheduled workflows using cron expressions",
      tags=["scheduling", "cron", "automation", "recurring"],
      examples=[
        "List all cron workflows in the 'batch' namespace",
        "Create a cron workflow that runs daily backup at 2 AM",
        "Get details of cron workflow 'weekly-reports'",
        "Update cron workflow 'daily-cleanup' schedule to run twice daily",
        "Suspend cron workflow 'maintenance-tasks' temporarily",
        "Resume suspended cron workflow 'log-rotation'",
        "Delete cron workflow 'obsolete-sync'",
        "Lint cron workflow specification before deployment",
      ],
    ),
    AgentSkill(
      id="archived_workflows",
      name="Archived Workflows",
      description="Access and manage historical workflow data and completed executions",
      tags=["history", "archives", "completed", "analysis"],
      examples=[
        "List archived workflows from the past month",
        "Get details of archived workflow with specific UID",
        "Search archived workflows by label selector 'app=data-pipeline'",
        "Delete old archived workflows to free up storage",
        "Resubmit failed archived workflow 'data-migration-v1'",
        "Retry archived workflow 'payment-processing' with same parameters",
        "Get archived workflow label keys for filtering",
        "Get available label values for archived workflow queries",
      ],
    ),
    AgentSkill(
      id="event_driven_automation",
      name="Event-Driven Automation",
      description="Manage event sources and sensors for reactive workflow automation",
      tags=["events", "sensors", "reactive", "automation"],
      examples=[
        "List all event sources in the 'monitoring' namespace",
        "Create webhook event source for CI/CD triggers",
        "Get details of event source 'github-webhooks'",
        "Update event source 'prometheus-alerts' configuration",
        "Delete unused event source 'legacy-notifications'",
        "List all sensors in the 'automation' namespace",
        "Create sensor to trigger workflows from Slack messages",
        "Get details of sensor 'deployment-trigger'",
        "Update sensor 'alert-responder' with new conditions",
        "Delete sensor 'test-sensor' after validation",
        "Receive and process external events",
        "List workflow event bindings for debugging",
      ],
    ),
    AgentSkill(
      id="monitoring_observability",
      name="Monitoring & Observability",
      description="Access logs, artifacts, and monitoring data for workflows",
      tags=["logs", "artifacts", "monitoring", "debugging"],
      examples=[
        "Get logs for workflow 'data-processing-job'",
        "Get logs for specific pod in workflow 'multi-step-pipeline'",
        "Download output artifacts from workflow 'ml-training'",
        "Get input artifacts used by workflow 'data-validation'",
        "Get artifacts by workflow UID for historical analysis",
        "Stream real-time logs from running workflow",
        "Watch workflow events as they happen",
        "Monitor event source logs for troubleshooting",
        "Watch sensor logs for debugging triggers",
      ],
    ),
    AgentSkill(
      id="system_information",
      name="System Information",
      description="Access Argo Workflows server information and user details",
      tags=["system", "info", "version", "user"],
      examples=[
        "Get Argo Workflows server version and build information",
        "Get current user information and permissions",
        "Get server info including supported features",
        "Check API server health and status",
        "Collect system events for diagnostics",
      ],
    ),
  ]

  return AgentCard(
    name="Argo_workflows Agent",
    description="Auto-generated A2A wrapper for Argo_workflows MCP server.",
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
