"""Model for AnalyticsRawIncidentResponses"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsrawincidentresponses(BaseModel):
    """Analyticsrawincidentresponses model"""

    responder_name: Optional[str] = None
    """Name of the user associated with the Incident Response."""
    responder_id: Optional[str] = None
    """ID of the user associated with the Incident Response."""
    response_status: Optional[str] = None
    """Status of the user's interaction with the Incident notification."""
    responder_type: Optional[str] = None
    """Type of responder, where `assigned` means the user was added to the Incident via Assignment at Incident creation,
`reassigned` means the user was added to the Incident via Reassignment, `escalated` means the user was added via Escalation,
and `added_responder` means the user was added via Responder Reqeuest."""
    requested_at: Optional[str] = None
    """Timestamp of when the user was requested."""
    responded_at: Optional[str] = None
    """Timestamp of when the user responded to the request."""
    time_to_respond_seconds: Optional[int] = None
    """Measures the time it took for the user to respond to the Incident request. In other words, `responded_at - requested_at`."""

class AnalyticsrawincidentresponsesResponse(APIResponse):
    """Response model for Analyticsrawincidentresponses"""
    data: Optional[Analyticsrawincidentresponses] = None

class AnalyticsrawincidentresponsesListResponse(APIResponse):
    """List response model for Analyticsrawincidentresponses"""
    data: List[Analyticsrawincidentresponses] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
