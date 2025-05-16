"""Model for IncidentAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentaction(BaseModel):
    """An incident action is a pending change to an incident that will automatically happen at some future time."""

    type: str
    at: str
    to: Optional[str] = None
    """The urgency that the incident will change to. This field is only present when the type is `urgency_change`."""

class IncidentactionResponse(APIResponse):
    """Response model for Incidentaction"""
    data: Optional[Incidentaction] = None

class IncidentactionListResponse(APIResponse):
    """List response model for Incidentaction"""
    data: List[Incidentaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
