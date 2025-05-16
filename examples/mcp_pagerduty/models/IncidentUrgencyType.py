"""Model for IncidentUrgencyType"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenturgencytype(BaseModel):
    """Incidenturgencytype model"""

    type: Optional[str] = None
    """The type of incident urgency: whether it's constant, or it's dependent on the support hours."""
    urgency: Optional[str] = None
    """The incidents' urgency, if type is constant."""

class IncidenturgencytypeResponse(APIResponse):
    """Response model for Incidenturgencytype"""
    data: Optional[Incidenturgencytype] = None

class IncidenturgencytypeListResponse(APIResponse):
    """List response model for Incidenturgencytype"""
    data: List[Incidenturgencytype] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
