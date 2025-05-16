"""Model for AnalyticsRawIncident"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsrawincident(BaseModel):
    """Analyticsrawincident model"""

    acknowledged_user_ids: Optional[List[str]] = None
    """The IDs of the users who acknowledged the incident."""
    acknowledged_user_names: Optional[List[str]] = None
    """The names of the users who acknowledged the incident."""
    acknowledgement_count: Optional[int] = None
    """Total count of acknowledgements in the incident."""
    active_user_count: Optional[int] = None
    """Total number of responders who either acknowledged the incident or accepted a responder request."""
    assigned_user_ids: Optional[List[str]] = None
    """The IDs of the users who were assigned the incident."""
    assigned_user_names: Optional[List[str]] = None
    """The names of the users who were assigned the incident."""
    assignment_count: Optional[int] = None
    """Total count of instances where responders were assigned an incident (including through reassignment or escalation)."""
    auto_resolved: Optional[bool] = None
    """Whether or not the incident resolved automatically, either via an integration 
or [auto-resolved in PagerDuty](https://support.pagerduty.com/docs/configurable-service-settings#auto-resolution)."""
    business_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during business hours; 8am-6pm Mon-Fri, based on the user’s time zone."""
    created_at: Optional[str] = None
    """Timestamp of when the incident was created."""
    updated_at: Optional[str] = None
    """Timestamp of when the incident was last updated by the analytics process.  Does not match the updated_at for an incident returned by the standard REST api incidents endpoint."""
    description: Optional[str] = None
    """The incident description"""
    engaged_seconds: Optional[int] = None
    """Total engaged time across all responders for this incident.  Engaged time is measured from the time a user engages with an incident (by acknowledging or accepting a responder request) until the incident is resolved.  This may include periods in which the incidents were snoozed."""
    engaged_user_count: Optional[int] = None
    """Total number of users who engaged (acknowledged, accepted responder request) in the incident."""
    escalation_count: Optional[int] = None
    """Total count of instances where an incident is escalated between responders assigned to an escalation policy."""
    escalation_policy_id: Optional[str] = None
    """ID of the escalation policy the incident was assigned to."""
    escalation_policy_name: Optional[str] = None
    """Name of the escalation policy the incident was assigned to."""
    id: Optional[str] = None
    """Incident ID"""
    incident_number: Optional[int] = None
    """The PagerDuty incident number."""
    incident_type_id: Optional[str] = None
    """ID of the Incident Type."""
    incident_type_name: Optional[str] = None
    """The name of the Incident Type."""
    joined_user_ids: Optional[List[str]] = None
    """The IDs of the users who either acknowledged the incident or accepted a responder request."""
    joined_user_names: Optional[List[str]] = None
    """The names of the users who either acknowledged the incident or accepted a responder request."""
    major: Optional[bool] = None
    """An incident is classified as a [major incident](https://support.pagerduty.com/docs/operational-reviews#major-incidents) if it has one of the two highest priorities, or if multiple responders are added and acknowledge the incident."""
    manual_escalation_count: Optional[int] = None
    """Total count of manual escalations in the incident."""
    off_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during off hours; 6pm-10pm Mon-Fri and all day Sat-Sun, based on the user’s time zone."""
    priority_id: Optional[str] = None
    """ID of the incident's priority level."""
    priority_name: Optional[str] = None
    """The user-provided short name of the priority."""
    priority_order: Optional[int] = None
    """The numerical value used to sort priorities. Higher values are higher priority."""
    reassignment_count: Optional[int] = None
    """Total count of reassignments in the incident."""
    resolved_at: Optional[str] = None
    """Timestamp of when the incident was resolved."""
    resolved_by_user_id: Optional[str] = None
    """ID of the user who resolved the incident."""
    resolved_by_user_name: Optional[str] = None
    """Name of the user who resolved the incident."""
    seconds_to_engage: Optional[int] = None
    """A measure of *people response time*. This metric measures the time from
the first user engagement (acknowledge or responder accept) to the last.
This metric is only used for incidents with **multiple responders**;
for incidents with one or no engaged users, this value is null."""
    seconds_to_first_ack: Optional[int] = None
    """Time between the start of an incident, and the first responder to acknowledge."""
    seconds_to_mobilize: Optional[int] = None
    """Time between the start of an incident, and the last additional responder to acknowledge. If an incident has one or no responders, the value will be null."""
    seconds_to_resolve: Optional[int] = None
    """Time from when an incident was triggered until it was resolved."""
    service_id: Optional[str] = None
    """ID of the service that the incident triggered on."""
    service_name: Optional[str] = None
    """Name of the service that the incident triggered on."""
    sleep_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during sleep hours; 10pm-8am every day, based on the user’s time zone."""
    snoozed_seconds: Optional[int] = None
    """Total seconds the incident has been snoozed for."""
    status: Optional[str] = None
    """The incident status. Can be one of `triggered`, `acknowledged`, or `resolved`."""
    team_id: Optional[str] = None
    """ID of the team the incident was assigned to."""
    team_name: Optional[str] = None
    """Name of the team the incident was assigned to."""
    timeout_escalation_count: Optional[int] = None
    """Total count of timeout escalations in the incident."""
    total_interruptions: Optional[int] = None
    """Total number of unique interruptions in the incident."""
    total_notifications: Optional[int] = None
    """Total number of notifications sent for the incident."""
    urgency: Optional[str] = None
    """Notification level"""
    user_defined_effort_seconds: Optional[int] = None
    """The total response effort in seconds,
[as defined by the user](https://support.pagerduty.com/docs/editing-incidents#edit-incident-duration)."""

class AnalyticsrawincidentResponse(APIResponse):
    """Response model for Analyticsrawincident"""
    data: Optional[Analyticsrawincident] = None

class AnalyticsrawincidentListResponse(APIResponse):
    """List response model for Analyticsrawincident"""
    data: List[Analyticsrawincident] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
