"""Model for IncidentAddon"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentaddon(BaseModel):
    """Incidentaddon model"""


class IncidentaddonResponse(APIResponse):
    """Response model for Incidentaddon"""
    data: Optional[Incidentaddon] = None

class IncidentaddonListResponse(APIResponse):
    """List response model for Incidentaddon"""
    data: List[Incidentaddon] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
