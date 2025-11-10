# Copyright 2025 CNOE
"""Launch an A2A HTTP server exposing the Argocd agent."""

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

from .agent_executor import ArgocdAgentExecutor

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
      id="application_management",
      name="Application Management",
      description="Core application operations for creating, managing, and monitoring ArgoCD applications",
      tags=["applications", "deployment", "lifecycle", "management"],
      examples=[
        "List all applications in ArgoCD",
        "Get the status and details of application 'my-app'",
        "Create a new application from a Git repository",
        "Delete application 'old-app' from the cluster",
        "Sync application 'my-service' to the latest Git commit",
        "Hard refresh application 'data-api' to force sync",
        "Rollback application 'web-frontend' to previous version",
        "Terminate application operation for 'stuck-deployment'",
        "Get application sync status and health details",
        "Set application parameters and override values",
      ],
    ),
    AgentSkill(
      id="repository_management",
      name="Repository Management",
      description="Manage Git repositories and Helm chart repositories in ArgoCD",
      tags=["repositories", "git", "helm", "sources"],
      examples=[
        "List all configured repositories in ArgoCD",
        "Add a new Git repository to ArgoCD",
        "Get details of repository 'https://github.com/my-org/manifests'",
        "Update repository credentials for private repos",
        "Delete unused repository 'legacy-charts'",
        "Test repository connection and access",
        "Validate repository certificates and SSH keys",
        "List applications using specific repository",
      ],
    ),
    AgentSkill(
      id="cluster_management",
      name="Cluster Management",
      description="Manage destination Kubernetes clusters for application deployments",
      tags=["clusters", "destinations", "kubernetes", "connectivity"],
      examples=[
        "List all managed clusters in ArgoCD",
        "Add a new destination cluster for deployments",
        "Get cluster connection status and server info",
        "Update cluster credentials and certificates",
        "Remove cluster 'staging-k8s' from ArgoCD",
        "Test cluster connectivity and permissions",
        "Get cluster namespaces and available resources",
        "Check cluster RBAC permissions for ArgoCD",
      ],
    ),
    AgentSkill(
      id="project_management",
      name="Project Management",
      description="Manage ArgoCD projects for organizing applications with RBAC and policies",
      tags=["projects", "rbac", "policies", "organization"],
      examples=[
        "List all projects in ArgoCD",
        "Create a new project 'platform-services'",
        "Get project details and assigned resources",
        "Update project policies and RBAC rules",
        "Delete unused project 'legacy-apps'",
        "Add allowed Git repositories to project",
        "Set project destination clusters and namespaces",
        "Configure project sync windows and restrictions",
      ],
    ),
    AgentSkill(
      id="certificate_management",
      name="Certificate Management",
      description="Manage TLS certificates for repository and cluster connections",
      tags=["certificates", "tls", "security", "connections"],
      examples=[
        "List all TLS certificates in ArgoCD",
        "Add a new certificate for private Git repository",
        "Get certificate details and expiration status",
        "Update certificate for 'gitlab.company.com'",
        "Delete expired certificate for old repository",
        "Validate certificate chain and trust",
        "Import certificate bundle for enterprise Git servers",
      ],
    ),
    AgentSkill(
      id="account_management",
      name="Account Management",
      description="Manage user accounts, authentication, and authorization in ArgoCD",
      tags=["accounts", "users", "authentication", "authorization", "rbac"],
      examples=[
        "List all user accounts in ArgoCD",
        "Create a new user account 'developer'",
        "Get user account details and permissions",
        "Update user password and authentication settings",
        "Delete inactive user account 'former-employee'",
        "Check user permissions for specific resources",
        "Generate authentication tokens for service accounts",
        "Verify user can access projects and applications",
      ],
    ),
    AgentSkill(
      id="monitoring_observability",
      name="Monitoring & Observability",
      description="Access logs, events, and monitoring data for applications and ArgoCD system",
      tags=["logs", "events", "monitoring", "debugging", "observability"],
      examples=[
        "Get application deployment history and events",
        "View sync operation logs for application 'api-service'",
        "Monitor application health and resource status",
        "Get ArgoCD server logs for troubleshooting",
        "Track application sync failures and errors",
        "View resource events for deployed applications",
        "Monitor Git repository polling and fetch operations",
        "Get cluster connection and authentication logs",
      ],
    ),
    AgentSkill(
      id="system_information",
      name="System Information",
      description="Access ArgoCD server information, version details, and system status",
      tags=["system", "info", "version", "status", "health"],
      examples=[
        "Get ArgoCD server version and build information",
        "Check ArgoCD system health and component status",
        "Get server configuration and feature flags",
        "View ArgoCD resource usage and performance metrics",
        "Get API server capabilities and supported features",
        "Check ArgoCD database connection and status",
        "View system settings and global configurations",
      ],
    ),
  ]

  return AgentCard(
    name="Argocd Agent",
    description="Auto-generated A2A wrapper for Argocd MCP server.",
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
    agent_executor=ArgocdAgentExecutor(),
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
