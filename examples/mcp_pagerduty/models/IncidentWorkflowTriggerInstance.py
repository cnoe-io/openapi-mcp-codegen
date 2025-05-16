"""Model for IncidentWorkflowTriggerInstance"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflowtriggerinstance(BaseModel):
    """Incidentworkflowtriggerinstance model"""


class IncidentworkflowtriggerinstanceResponse(APIResponse):
    """Response model for Incidentworkflowtriggerinstance"""
    data: Optional[Incidentworkflowtriggerinstance] = None

class IncidentworkflowtriggerinstanceListResponse(APIResponse):
    """List response model for Incidentworkflowtriggerinstance"""
    data: List[Incidentworkflowtriggerinstance] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
