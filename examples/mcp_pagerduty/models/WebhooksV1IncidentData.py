"""Model for WebhooksV1IncidentData"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksv1incidentdata(BaseModel):
    """The incident details at the time of the state change."""

    id: Optional[str] = None
    incident_number: Optional[int] = None
    """The number of the incident. This is unique across the account."""
    created_on: Optional[str] = None
    """The date/time the incident was first triggered."""
    status: Optional[str] = None
    """The current status of the incident."""
    html_url: Optional[str] = None
    incident_key: Optional[str] = None
    """The incident's de-duplication key."""
    service: Optional[str] = None
    assigned_to_user: Optional[str] = None
    assigned_to: Optional[List[str]] = None
    trigger_summary_data: Optional[Dict] = None
    trigger_details_html_url: Optional[str] = None
    last_status_change_on: Optional[str] = None
    """The time at which the status of the incident last changed."""
    last_status_change_by: Optional[str] = None
    number_of_escalations: Optional[int] = None
    """Number of times the incident has been escalated."""
    urgency: Optional[str] = None

class Webhooksv1incidentdataResponse(APIResponse):
    """Response model for Webhooksv1incidentdata"""
    data: Optional[Webhooksv1incidentdata] = None

class Webhooksv1incidentdataListResponse(APIResponse):
    """List response model for Webhooksv1incidentdata"""
    data: List[Webhooksv1incidentdata] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
