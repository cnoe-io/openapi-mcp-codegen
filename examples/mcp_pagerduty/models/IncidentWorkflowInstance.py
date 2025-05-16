"""Model for IncidentWorkflowInstance"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflowinstance(BaseModel):
    """Incidentworkflowinstance model"""

    id: Optional[str] = None
    type: Optional[str] = None
    """A string that determines the schema of the object. This must be the standard name for the entity, suffixed by `_reference` if the object is a reference."""
    incident: Optional[str] = None

class IncidentworkflowinstanceResponse(APIResponse):
    """Response model for Incidentworkflowinstance"""
    data: Optional[Incidentworkflowinstance] = None

class IncidentworkflowinstanceListResponse(APIResponse):
    """List response model for Incidentworkflowinstance"""
    data: List[Incidentworkflowinstance] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
