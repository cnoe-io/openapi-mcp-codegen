"""Model for IncidentReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentreference(BaseModel):
    """Incidentreference model"""


class IncidentreferenceResponse(APIResponse):
    """Response model for Incidentreference"""
    data: Optional[Incidentreference] = None

class IncidentreferenceListResponse(APIResponse):
    """List response model for Incidentreference"""
    data: List[Incidentreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
