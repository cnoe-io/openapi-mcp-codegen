"""Model for IncidentType"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenttype(BaseModel):
    """Incidenttype model"""

    enabled: Optional[bool] = None
    """State of this Incident Type object."""
    id: Optional[str] = None
    name: Optional[str] = None
    """The name of the Incident Type."""
    parent: Optional[Dict] = None
    """The parent Incident Type (id/name). If omitted, type is created under top level (incident_default)"""
    type: Optional[str] = None
    """A string that determines the schema of the object. This must be the standard name for the entity, suffixed by `_reference` if the object is a reference."""
    description: Optional[str] = None
    """A succinct description of the Incident Type."""
    created_at: Optional[str] = None
    """The time the Incident Type was created."""
    updated_at: Optional[str] = None
    """The time the Incident Type was last modified."""
    display_name: Optional[str] = None
    """The display name of the Incident Type. The first character must be alphanumeric. Max length: 50, Min Length : 1. The `display_name` for a Field must be unique."""

class IncidenttypeResponse(APIResponse):
    """Response model for Incidenttype"""
    data: Optional[Incidenttype] = None

class IncidenttypeListResponse(APIResponse):
    """List response model for Incidenttype"""
    data: List[Incidenttype] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
