"""Model for IncidentsRespondersReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentsrespondersreference(BaseModel):
    """Incidentsrespondersreference model"""

    state: Optional[str] = None
    """The status of the responder being added to the incident"""
    user: Optional[str] = None
    incident: Optional[str] = None
    updated_at: Optional[str] = None
    message: Optional[str] = None
    """The message sent with the responder request"""
    requester: Optional[str] = None
    requested_at: Optional[str] = None

class IncidentsrespondersreferenceResponse(APIResponse):
    """Response model for Incidentsrespondersreference"""
    data: Optional[Incidentsrespondersreference] = None

class IncidentsrespondersreferenceListResponse(APIResponse):
    """List response model for Incidentsrespondersreference"""
    data: List[Incidentsrespondersreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
