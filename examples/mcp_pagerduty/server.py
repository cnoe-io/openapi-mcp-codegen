#!/usr/bin/env python3
"""
PagerDuty  MCP Server

This server provides a Model Context Protocol (MCP) interface to the PagerDuty ,
allowing large language models and AI assistants to interact with the service.
"""
import logging
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import tools
from agent_pagerduty.pagerduty_mcp.tools import abilities
from agent_pagerduty.pagerduty_mcp.tools import addons
from agent_pagerduty.pagerduty_mcp.tools import alert_grouping_settings
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_all
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_escalation_policies
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_escalation_policies_all
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_services
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_services_all
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_teams
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_incidents_teams_all
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_pd_advance_usage_features
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_responders_all
from agent_pagerduty.pagerduty_mcp.tools import analytics_metrics_responders_teams
from agent_pagerduty.pagerduty_mcp.tools import analytics_raw_incidents
from agent_pagerduty.pagerduty_mcp.tools import audit_records
from agent_pagerduty.pagerduty_mcp.tools import automation_actions_actions
from agent_pagerduty.pagerduty_mcp.tools import automation_actions_invocations
from agent_pagerduty.pagerduty_mcp.tools import automation_actions_runners
from agent_pagerduty.pagerduty_mcp.tools import business_services
from agent_pagerduty.pagerduty_mcp.tools import business_services_impactors
from agent_pagerduty.pagerduty_mcp.tools import business_services_impacts
from agent_pagerduty.pagerduty_mcp.tools import business_services_priority_thresholds
from agent_pagerduty.pagerduty_mcp.tools import change_events
from agent_pagerduty.pagerduty_mcp.tools import escalation_policies
from agent_pagerduty.pagerduty_mcp.tools import event_orchestrations
from agent_pagerduty.pagerduty_mcp.tools import extension_schemas
from agent_pagerduty.pagerduty_mcp.tools import extensions
from agent_pagerduty.pagerduty_mcp.tools import incident_workflows
from agent_pagerduty.pagerduty_mcp.tools import incident_workflows_actions
from agent_pagerduty.pagerduty_mcp.tools import incident_workflows_triggers
from agent_pagerduty.pagerduty_mcp.tools import incidents
from agent_pagerduty.pagerduty_mcp.tools import incidents_count
from agent_pagerduty.pagerduty_mcp.tools import incidents_types
from agent_pagerduty.pagerduty_mcp.tools import incidents_custom_fields
from agent_pagerduty.pagerduty_mcp.tools import license_allocations
from agent_pagerduty.pagerduty_mcp.tools import licenses
from agent_pagerduty.pagerduty_mcp.tools import log_entries
from agent_pagerduty.pagerduty_mcp.tools import maintenance_windows
from agent_pagerduty.pagerduty_mcp.tools import notifications
from agent_pagerduty.pagerduty_mcp.tools import oauth_delegations
from agent_pagerduty.pagerduty_mcp.tools import oauth_delegations_revocation_requests_status
from agent_pagerduty.pagerduty_mcp.tools import oncalls
from agent_pagerduty.pagerduty_mcp.tools import paused_incident_reports_alerts
from agent_pagerduty.pagerduty_mcp.tools import paused_incident_reports_counts
from agent_pagerduty.pagerduty_mcp.tools import priorities
from agent_pagerduty.pagerduty_mcp.tools import response_plays
from agent_pagerduty.pagerduty_mcp.tools import rulesets
from agent_pagerduty.pagerduty_mcp.tools import schedules
from agent_pagerduty.pagerduty_mcp.tools import schedules_preview
from agent_pagerduty.pagerduty_mcp.tools import service_dependencies_associate
from agent_pagerduty.pagerduty_mcp.tools import service_dependencies_disassociate
from agent_pagerduty.pagerduty_mcp.tools import services
from agent_pagerduty.pagerduty_mcp.tools import services_custom_fields
from agent_pagerduty.pagerduty_mcp.tools import standards
from agent_pagerduty.pagerduty_mcp.tools import status_dashboards
from agent_pagerduty.pagerduty_mcp.tools import status_pages
from agent_pagerduty.pagerduty_mcp.tools import tags
from agent_pagerduty.pagerduty_mcp.tools import teams
from agent_pagerduty.pagerduty_mcp.tools import templates
from agent_pagerduty.pagerduty_mcp.tools import templates_fields
from agent_pagerduty.pagerduty_mcp.tools import users
from agent_pagerduty.pagerduty_mcp.tools import users_me
from agent_pagerduty.pagerduty_mcp.tools import vendors
from agent_pagerduty.pagerduty_mcp.tools import webhook_subscriptions
from agent_pagerduty.pagerduty_mcp.tools import workflows_integrations
from agent_pagerduty.pagerduty_mcp.tools import workflows_integrations_connections

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("PagerDuty  MCP Server")

# Register tools
# Register abilities tools
mcp.tool()(abilities.listAbilities)

# Register addons tools
mcp.tool()(addons.createAddon)
mcp.tool()(addons.listAddon)

# Register alert_grouping_settings tools
mcp.tool()(alert_grouping_settings.postAlertGroupingSettings)
mcp.tool()(alert_grouping_settings.listAlertGroupingSettings)

# Register analytics_metrics_incidents_all tools
mcp.tool()(analytics_metrics_incidents_all.getAnalyticsMetricsIncidentsAll)

# Register analytics_metrics_incidents_escalation_policies tools
mcp.tool()(analytics_metrics_incidents_escalation_policies.getAnalyticsMetricsIncidentsEscalationPolicy)

# Register analytics_metrics_incidents_escalation_policies_all tools
mcp.tool()(analytics_metrics_incidents_escalation_policies_all.getAnalyticsMetricsIncidentsEscalationPolicyAll)

# Register analytics_metrics_incidents_services tools
mcp.tool()(analytics_metrics_incidents_services.getAnalyticsMetricsIncidentsService)

# Register analytics_metrics_incidents_services_all tools
mcp.tool()(analytics_metrics_incidents_services_all.getAnalyticsMetricsIncidentsServiceAll)

# Register analytics_metrics_incidents_teams tools
mcp.tool()(analytics_metrics_incidents_teams.getAnalyticsMetricsIncidentsTeam)

# Register analytics_metrics_incidents_teams_all tools
mcp.tool()(analytics_metrics_incidents_teams_all.getAnalyticsMetricsIncidentsTeamAll)

# Register analytics_metrics_pd_advance_usage_features tools
mcp.tool()(analytics_metrics_pd_advance_usage_features.getAnalyticsMetricsPdAdvanceUsageFeatures)

# Register analytics_metrics_responders_all tools
mcp.tool()(analytics_metrics_responders_all.getAnalyticsMetricsRespondersAll)

# Register analytics_metrics_responders_teams tools
mcp.tool()(analytics_metrics_responders_teams.getAnalyticsMetricsRespondersTeam)

# Register analytics_raw_incidents tools
mcp.tool()(analytics_raw_incidents.getAnalyticsIncidents)

# Register audit_records tools
mcp.tool()(audit_records.listAuditRecords)

# Register automation_actions_actions tools
mcp.tool()(automation_actions_actions.getAllAutomationActions)
mcp.tool()(automation_actions_actions.createAutomationAction)

# Register automation_actions_invocations tools
mcp.tool()(automation_actions_invocations.listAutomationActionInvocations)

# Register automation_actions_runners tools
mcp.tool()(automation_actions_runners.getAutomationActionsRunners)
mcp.tool()(automation_actions_runners.createAutomationActionsRunner)

# Register business_services tools
mcp.tool()(business_services.createBusinessService)
mcp.tool()(business_services.listBusinessServices)

# Register business_services_impactors tools
mcp.tool()(business_services_impactors.getBusinessServiceTopLevelImpactors)

# Register business_services_impacts tools
mcp.tool()(business_services_impacts.getBusinessServiceImpacts)

# Register business_services_priority_thresholds tools
mcp.tool()(business_services_priority_thresholds.getBusinessServicePriorityThresholds)
mcp.tool()(business_services_priority_thresholds.deleteBusinessServicePriorityThresholds)
mcp.tool()(business_services_priority_thresholds.putBusinessServicePriorityThresholds)

# Register change_events tools
mcp.tool()(change_events.listChangeEvents)
mcp.tool()(change_events.createChangeEvent)

# Register escalation_policies tools
mcp.tool()(escalation_policies.listEscalationPolicies)
mcp.tool()(escalation_policies.createEscalationPolicy)

# Register event_orchestrations tools
mcp.tool()(event_orchestrations.listEventOrchestrations)
mcp.tool()(event_orchestrations.postOrchestration)

# Register extension_schemas tools
mcp.tool()(extension_schemas.listExtensionSchemas)

# Register extensions tools
mcp.tool()(extensions.createExtension)
mcp.tool()(extensions.listExtensions)

# Register incident_workflows tools
mcp.tool()(incident_workflows.listIncidentWorkflows)
mcp.tool()(incident_workflows.postIncidentWorkflow)

# Register incident_workflows_actions tools
mcp.tool()(incident_workflows_actions.listIncidentWorkflowActions)

# Register incident_workflows_triggers tools
mcp.tool()(incident_workflows_triggers.createIncidentWorkflowTrigger)
mcp.tool()(incident_workflows_triggers.listIncidentWorkflowTriggers)

# Register incidents tools
mcp.tool()(incidents.createIncident)
mcp.tool()(incidents.updateIncidents)
mcp.tool()(incidents.listIncidents)

# Register incidents_count tools

# Register incidents_types tools
mcp.tool()(incidents_types.createIncidentType)
mcp.tool()(incidents_types.listIncidentTypes)

# Register incidents_custom_fields tools
mcp.tool()(incidents_custom_fields.listCustomFieldsFields)
mcp.tool()(incidents_custom_fields.createCustomFieldsField)

# Register license_allocations tools
mcp.tool()(license_allocations.listLicenseAllocations)

# Register licenses tools
mcp.tool()(licenses.listLicenses)

# Register log_entries tools
mcp.tool()(log_entries.listLogEntries)

# Register maintenance_windows tools
mcp.tool()(maintenance_windows.listMaintenanceWindows)
mcp.tool()(maintenance_windows.createMaintenanceWindow)

# Register notifications tools
mcp.tool()(notifications.listNotifications)

# Register oauth_delegations tools
mcp.tool()(oauth_delegations.deleteOauthDelegations)

# Register oauth_delegations_revocation_requests_status tools
mcp.tool()(oauth_delegations_revocation_requests_status.getOauthDelegationsRevocationRequestsStatus)

# Register oncalls tools
mcp.tool()(oncalls.listOnCalls)

# Register paused_incident_reports_alerts tools
mcp.tool()(paused_incident_reports_alerts.getPausedIncidentReportAlerts)

# Register paused_incident_reports_counts tools
mcp.tool()(paused_incident_reports_counts.getPausedIncidentReportCounts)

# Register priorities tools
mcp.tool()(priorities.listPriorities)

# Register response_plays tools
mcp.tool()(response_plays.createResponsePlay)
mcp.tool()(response_plays.listResponsePlays)

# Register rulesets tools
mcp.tool()(rulesets.listRulesets)
mcp.tool()(rulesets.createRuleset)

# Register schedules tools
mcp.tool()(schedules.listSchedules)
mcp.tool()(schedules.createSchedule)

# Register schedules_preview tools
mcp.tool()(schedules_preview.createSchedulePreview)

# Register service_dependencies_associate tools
mcp.tool()(service_dependencies_associate.createServiceDependency)

# Register service_dependencies_disassociate tools
mcp.tool()(service_dependencies_disassociate.deleteServiceDependency)

# Register services tools
mcp.tool()(services.listServices)
mcp.tool()(services.createService)

# Register services_custom_fields tools
mcp.tool()(services_custom_fields.createServiceCustomField)
mcp.tool()(services_custom_fields.listServiceCustomFields)

# Register standards tools
mcp.tool()(standards.listStandards)

# Register status_dashboards tools
mcp.tool()(status_dashboards.listStatusDashboards)

# Register status_pages tools
mcp.tool()(status_pages.listStatusPages)

# Register tags tools
mcp.tool()(tags.createTags)
mcp.tool()(tags.listTags)

# Register teams tools
mcp.tool()(teams.createTeam)
mcp.tool()(teams.listTeams)

# Register templates tools
mcp.tool()(templates.createTemplate)
mcp.tool()(templates.getTemplates)

# Register templates_fields tools
mcp.tool()(templates_fields.getTemplateFields)

# Register users tools
mcp.tool()(users.createUser)
mcp.tool()(users.listUsers)

# Register users_me tools
mcp.tool()(users_me.getCurrentUser)

# Register vendors tools
mcp.tool()(vendors.listVendors)

# Register webhook_subscriptions tools
mcp.tool()(webhook_subscriptions.createWebhookSubscription)
mcp.tool()(webhook_subscriptions.listWebhookSubscriptions)

# Register workflows_integrations tools
mcp.tool()(workflows_integrations.listWorkflowIntegrations)

# Register workflows_integrations_connections tools
mcp.tool()(workflows_integrations_connections.listWorkflowIntegrationConnections)


# Start server when run directly
if __name__ == "__main__":
    mcp.run()
