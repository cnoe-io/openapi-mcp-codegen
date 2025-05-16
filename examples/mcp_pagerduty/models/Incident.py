"""Model for Incident"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incident(BaseModel):
    """Incident model"""


class IncidentResponse(APIResponse):
    """Response model for Incident"""
    data: Optional[Incident] = None

class IncidentListResponse(APIResponse):
    """List response model for Incident"""
    data: List[Incident] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
