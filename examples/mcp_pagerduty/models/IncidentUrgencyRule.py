"""Model for IncidentUrgencyRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenturgencyrule(BaseModel):
    """Incidenturgencyrule model"""


class IncidenturgencyruleResponse(APIResponse):
    """Response model for Incidenturgencyrule"""
    data: Optional[Incidenturgencyrule] = None

class IncidenturgencyruleListResponse(APIResponse):
    """List response model for Incidenturgencyrule"""
    data: List[Incidenturgencyrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
