"""Model for IncidentWorkflow"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflow(BaseModel):
    """Incidentworkflow model"""


class IncidentworkflowResponse(APIResponse):
    """Response model for Incidentworkflow"""
    data: Optional[Incidentworkflow] = None

class IncidentworkflowListResponse(APIResponse):
    """List response model for Incidentworkflow"""
    data: List[Incidentworkflow] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
