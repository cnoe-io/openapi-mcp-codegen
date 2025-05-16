"""Model for AnalyticsIncidentMetricsEscalationPolicy"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsincidentmetricsescalationpolicy(BaseModel):
    """Analyticsincidentmetricsescalationpolicy model"""

    distinct_responder_count: Optional[int] = None
    """Distinct count of responders who engaged in incidents on the escalation policy"""
    escalation_policy_id: Optional[str] = None
    """ID of the escalation policy the incident was last assigned to. Not included when aggregating by all."""
    escalation_policy_name: Optional[str] = None
    """Name of the escalation policy the incident was last assigned to. Not included when aggregating by all."""
    mean_assignment_count: Optional[int] = None
    """Mean count of instances where responders were assigned an incident (including through reassignment or escalation) or accepted a responder request."""
    mean_engaged_seconds: Optional[int] = None
    """Mean engaged time across all responders.
Engaged time is measured from the time a user engages with an incident (by
acknowledging or accepting a responder request) until the incident is resolved.
This may include periods in which the incidents were snoozed."""
    mean_engaged_user_count: Optional[int] = None
    """Mean number of users who engaged with an incident. *Engaged* is defined as
acknowledging an incident or accepting a responder request in it."""
    mean_seconds_to_engage: Optional[int] = None
    """A measure of *people response time*. This metric measures the time from
the first user engagement (acknowledge or responder accept) to the last.
This metric is only used for incidents with **multiple responders**;
for incidents with one or no engaged users, this value is null."""
    mean_seconds_to_first_ack: Optional[int] = None
    """Mean time between the start of an incident, and the first responder to acknowledge."""
    mean_seconds_to_mobilize: Optional[int] = None
    """Mean time between the start of an incident, and the last additional responder
to acknowledge. For incidents with one or no engaged users, this value is null."""
    mean_seconds_to_resolve: Optional[int] = None
    """Mean time from when an incident was triggered until it was resolved."""
    mean_user_defined_engaged_seconds: Optional[int] = None
    """Mean engaged time across all responders. Engaged time is measured from the time 
a user engages with an incident (by acknowledging or accepting a responder request) 
until the incident is resolved. This may include periods in which the incidents were snoozed.
This metric uses the incident response effort values that 
[users have defined](https://support.pagerduty.com/docs/edit-incidents#edit-incident-duration),
if they exist."""
    range_start: Optional[str] = None
    """Start of the date range that the metrics were calculated for. Only included when an aggregate unit is specified in the request."""
    team_id: Optional[str] = None
    """ID of the team the incident was assigned to. Not included when aggregating by all."""
    team_name: Optional[str] = None
    """Name of the team the incident was assigned to. Not included when aggregating by all."""
    total_business_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during business hours; 8am-6pm Mon-Fri, based on the user’s time zone."""
    total_engaged_seconds: Optional[int] = None
    """Total engaged time across all responders. Engaged time is measured from
the time a user engages with an incident (by acknowledging or accepting a responder request)
until the incident is resolved. This may include periods in which the incidents were snoozed."""
    total_escalation_count: Optional[int] = None
    """Total count of instances where an incident is escalated between responders
assigned to an escalation policy."""
    total_incident_count: Optional[int] = None
    """The total number of incidents that were created."""
    total_incidents_acknowledged: Optional[int] = None
    """The total count of assigned incidents acknowledged. 
Only explicit incident acknowledgment counts; reassign, resolve, and escalation actions do not imply acknowledgement."""
    total_incidents_auto_resolved: Optional[str] = None
    """The total count of incidents that were resolved automatically. 
This count includes incidents resolved via an integration and those that were [auto-resolved in PagerDuty](https://support.pagerduty.com/docs/configurable-service-settings#auto-resolution)."""
    total_incidents_manual_escalated: Optional[int] = None
    """The total count of incidents that were manually escalated."""
    total_incidents_reassigned: Optional[int] = None
    """The total count of incidents that were reassigned."""
    total_incidents_timeout_escalated: Optional[int] = None
    """The total count of incidents that were escalated due to timeouts."""
    total_interruptions: Optional[int] = None
    """Total number of unique interruptions."""
    total_notifications: Optional[int] = None
    """The total count of incident notifications sent via email, SMS, phone call and push."""
    total_off_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during off hours; 6pm-10pm Mon-Fri and all day Sat-Sun, based on the user’s time zone."""
    total_sleep_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during sleep hours; 10pm-8am every day, based on the user’s time zone."""
    total_snoozed_seconds: Optional[int] = None
    """Total number of seconds incidents were snoozed."""
    total_user_defined_engaged_seconds: Optional[int] = None
    """Total engaged time across all responders. Engaged time is measured from
the time a user engages with an incident (by acknowledging or accepting a responder request)
until the incident is resolved. This may include periods in which the incidents were snoozed.
This metric uses the edited incident response effort values that 
[users have defined](https://support.pagerduty.com/docs/edit-incidents#edit-incident-duration),
if they exist."""
    up_time_pct: Optional[float] = None
    """The percentage of time in the defined date range that the service was not interrupted
by a [major incident](https://support.pagerduty.com/docs/operational-reviews#major-incidents). Not included when aggregating by all."""

class AnalyticsincidentmetricsescalationpolicyResponse(APIResponse):
    """Response model for Analyticsincidentmetricsescalationpolicy"""
    data: Optional[Analyticsincidentmetricsescalationpolicy] = None

class AnalyticsincidentmetricsescalationpolicyListResponse(APIResponse):
    """List response model for Analyticsincidentmetricsescalationpolicy"""
    data: List[Analyticsincidentmetricsescalationpolicy] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
