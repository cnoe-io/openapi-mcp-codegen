"""Model for IncidentWorkflowTrigger"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflowtrigger(BaseModel):
    """Incidentworkflowtrigger model"""


class IncidentworkflowtriggerResponse(APIResponse):
    """Response model for Incidentworkflowtrigger"""
    data: Optional[Incidentworkflowtrigger] = None

class IncidentworkflowtriggerListResponse(APIResponse):
    """List response model for Incidentworkflowtrigger"""
    data: List[Incidentworkflowtrigger] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
