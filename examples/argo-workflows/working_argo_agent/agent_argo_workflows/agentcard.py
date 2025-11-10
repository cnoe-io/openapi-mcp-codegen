# Copyright 2025 CNOE Contributors
# SPDX-License-Identifier: Apache-2.0

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
AGENT_NAME = 'argo_workflows'
AGENT_DESCRIPTION = 'An AI agent that provides capabilities to manage, create, and monitor Argo Workflows.'

agent_skill = AgentSkill(
  id="argo_workflows_agent_skill",
  name="Argo Workflows Agent Skill",
  description="Provides capabilities to create, manage, and monitor Argo Workflows.",
  tags=[
    "argo-workflows",
    "workflows",
    "kubernetes",
    "ci/cd"],
  examples=[
      # Workflow Management
      "Create a simple hello-world workflow.",
      "List all workflows in the default namespace.",
      "Get the status of workflow 'my-workflow'.",
      "Delete workflow 'my-workflow'.",

      # Workflow Templates
      "Create a workflow template for CI/CD pipeline.",
      "List all workflow templates.",
      "Get details of workflow template 'ci-template'.",
      "Delete workflow template 'ci-template'.",

      # Cron Workflows
      "Create a cron workflow that runs daily at midnight.",
      "List all cron workflows.",
      "Get details of cron workflow 'daily-backup'.",
      "Suspend cron workflow 'daily-backup'.",
      "Resume cron workflow 'daily-backup'.",
      "Delete cron workflow 'daily-backup'.",

      # Cluster Workflow Templates
      "List all cluster workflow templates.",
      "Get details of cluster workflow template 'global-template'.",

      # Workflow Status and Logs
      "Get logs for workflow 'my-workflow'.",
      "Get artifacts from workflow 'my-workflow'.",
      "Retry failed workflow 'my-workflow'.",
      "Stop running workflow 'my-workflow'.",

      # Service Accounts and RBAC
      "List all service accounts.",
      "Get details of service account 'workflow-sa'.",

      # Workflow Events
      "Get events for workflow 'my-workflow'.",
      "Watch workflow events in real-time.",
  ])

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
  print("===================================")

  return AgentCard(
    name=AGENT_NAME,
    id=f'{AGENT_NAME.lower().replace("_", "-")}-tools-agent',
    description=AGENT_DESCRIPTION,
    url=agent_url,
    version='0.1.0',
    defaultInputModes=SUPPORTED_CONTENT_TYPES,
    defaultOutputModes=SUPPORTED_CONTENT_TYPES,
    capabilities=capabilities,
    skills=[agent_skill],
    # Using the security field instead of the non-existent AgentAuthentication class
    security=[{"public": []}],
  )
