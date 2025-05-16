"""Model for IncidentTypeReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenttypereference(BaseModel):
    """Incidenttypereference model"""

    id: Optional[str] = None
    name: Optional[str] = None
    """The name of the Incident Type."""

class IncidenttypereferenceResponse(APIResponse):
    """Response model for Incidenttypereference"""
    data: Optional[Incidenttypereference] = None

class IncidenttypereferenceListResponse(APIResponse):
    """List response model for Incidenttypereference"""
    data: List[Incidenttypereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
