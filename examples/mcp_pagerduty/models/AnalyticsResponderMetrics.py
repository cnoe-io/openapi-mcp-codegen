"""Model for AnalyticsResponderMetrics"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsrespondermetrics(BaseModel):
    """Analyticsrespondermetrics model"""

    mean_engaged_seconds: Optional[int] = None
    """Mean engaged time across all responders for incidents that match the given filters.
Engaged time is measured from the time a user engages with an incident (by
acknowledging or accepting a responder request) until the incident is resolved.
This may include periods in which the incidents were snoozed."""
    mean_time_to_acknowledge_seconds: Optional[int] = None
    """The average time between when an incident is first assigned to a user and when the incident is first acknowledged by that user.
Reassign, resolve, and escalation actions do not imply acknowledgement."""
    responder_id: Optional[int] = None
    """ID of the responder (user). Not included when aggregating by all responders."""
    responder_name: Optional[str] = None
    """Name of the responder (user). Not included when aggregating by all responders."""
    team_id: Optional[str] = None
    """ID of the team associated with the responder. Not included when aggregating by all responders."""
    team_name: Optional[str] = None
    """Name of the team associated with the responder. Not included when aggregating by all responders."""
    total_business_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during business hours; 8am-6pm Mon-Fri, based on the user’s time zone."""
    total_engaged_seconds: Optional[int] = None
    """Total engaged time across all responders for incidents. Engaged time is measured from
the time a user engages with an incident (by acknowledging or accepting a responder request)
until the incident is resolved. This may include periods in which the incidents were snoozed."""
    total_incident_count: Optional[int] = None
    """The total number of incidents that were created."""
    total_incidents_acknowledged: Optional[int] = None
    """The total count of assigned incidents acknowledged by the user. 
Only explicit incident acknowledgment counts; reassign, resolve, and escalation actions do not imply acknowledgement."""
    total_incidents_manual_escalated_from: Optional[int] = None
    """The total count of the user’s assigned incidents that were manually escalated away from a user without acknowledgement."""
    total_incidents_manual_escalated_to: Optional[int] = None
    """The total count of incidents the user was manually escalated to."""
    total_incidents_reassigned_from: Optional[int] = None
    """The total count of a user's assigned incidents that were reassigned away from the user to another user or escalation policy."""
    total_incidents_reassigned_to: Optional[int] = None
    """The total count of incidents the user was reassigned to."""
    total_incidents_timeout_escalated_from: Optional[int] = None
    """The total count of the user’s assigned incidents that were escalated due to timeouts."""
    total_incidents_timeout_escalated_to: Optional[int] = None
    """The total count of incidents the user was escalated to due to timeouts."""
    total_interruptions: Optional[int] = None
    """Total number of unique interruptions."""
    total_notifications: Optional[int] = None
    """The total count of incident notifications sent via email, SMS, phone call and push."""
    total_off_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during off hours; 6pm-10pm Mon-Fri and all day Sat-Sun, based on the user’s time zone."""
    total_seconds_on_call: Optional[int] = None
    """Total seconds the responder was on call."""
    total_seconds_on_call_level_1: Optional[int] = None
    """Total seconds the responder was on call at level 1 of their escalation policy."""
    total_seconds_on_call_level_2_plus: Optional[int] = None
    """Total seconds the responder was on call at level 2 or higher of their escalation policy."""
    total_sleep_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during sleep hours; 10pm-8am every day, based on the user’s time zone."""

class AnalyticsrespondermetricsResponse(APIResponse):
    """Response model for Analyticsrespondermetrics"""
    data: Optional[Analyticsrespondermetrics] = None

class AnalyticsrespondermetricsListResponse(APIResponse):
    """List response model for Analyticsrespondermetrics"""
    data: List[Analyticsrespondermetrics] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
