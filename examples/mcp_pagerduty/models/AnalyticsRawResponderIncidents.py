"""Model for AnalyticsRawResponderIncidents"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsrawresponderincidents(BaseModel):
    """Analyticsrawresponderincidents model"""

    incident_created_at: Optional[str] = None
    """Timestamp of when the incident was created."""
    incident_description: Optional[str] = None
    """The incident description."""
    incident_id: Optional[str] = None
    """Incident ID"""
    incident_number: Optional[int] = None
    """The PagerDuty incident number."""
    incident_priority_id: Optional[str] = None
    """ID of the incident's priority level."""
    incident_priority_name: Optional[str] = None
    """The user-provided short name of the priority."""
    incident_priority_order: Optional[int] = None
    """The numerical value used to sort priorities. Higher values are higher priority."""
    incident_urgency: Optional[str] = None
    """Notification level"""
    mean_time_to_acknowledge_seconds: Optional[int] = None
    """Mean time from this user being assigned to an incident until this user acknowledges the incident."""
    responder_id: Optional[str] = None
    """ID of the responder."""
    responder_name: Optional[str] = None
    """Name of the responder."""
    service_id: Optional[str] = None
    """ID of the service that the incident triggered on."""
    service_name: Optional[str] = None
    """Name of the service that the incident triggered on."""
    service_team_id: Optional[str] = None
    """ID of the team that owns the related service."""
    service_team_name: Optional[str] = None
    """Name of the team that owns the related service."""
    total_acknowledgements: Optional[int] = None
    """Total acknowledgements from the responder on the incident."""
    total_business_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during business hours; 8am-6pm Mon-Fri, based on the user’s time zone."""
    total_engaged_seconds: Optional[int] = None
    """Total engaged time across all responders for incidents. Engaged time is measured from
the time a user engages with an incident (by acknowledging or accepting a responder request)
until the incident is resolved. This may include periods in which the incidents were snoozed."""
    total_interruptions: Optional[int] = None
    """Total number of unique interruptions for the responder during the incident."""
    total_manual_escalations_from: Optional[int] = None
    """Total times the responder was manually escalated away from the incident."""
    total_manual_escalations_to: Optional[int] = None
    """Total times the responder was manually escalated to the incident."""
    total_off_hour_interruptions: Optional[str] = None
    """Total number of unique interruptions during off hours; 6pm-10pm Mon-Fri and all day Sat-Sun, based on the user’s time zone."""
    total_reassignments_from: Optional[int] = None
    """Total times the responder was reassigned away from the incident."""
    total_reassignments_to: Optional[int] = None
    """Total times the responder was reassigned to the incident."""
    total_sleep_hour_interruptions: Optional[int] = None
    """Total number of unique interruptions during sleep hours; 10pm-8am every day, based on the user’s time zone."""
    total_timeout_escalations_from: Optional[int] = None
    """Total times the responder was escalated away from the incident due to timeout."""
    total_timeout_escalations_to: Optional[int] = None
    """Total times the responder was escalated to the incident due to timeout."""

class AnalyticsrawresponderincidentsResponse(APIResponse):
    """Response model for Analyticsrawresponderincidents"""
    data: Optional[Analyticsrawresponderincidents] = None

class AnalyticsrawresponderincidentsListResponse(APIResponse):
    """List response model for Analyticsrawresponderincidents"""
    data: List[Analyticsrawresponderincidents] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
