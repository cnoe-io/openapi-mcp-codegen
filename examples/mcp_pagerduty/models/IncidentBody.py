"""Model for IncidentBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentbody(BaseModel):
    """Incidentbody model"""

    details: Optional[Dict] = None
    """Additional incident details."""

class IncidentbodyResponse(APIResponse):
    """Response model for Incidentbody"""
    data: Optional[Incidentbody] = None

class IncidentbodyListResponse(APIResponse):
    """List response model for Incidentbody"""
    data: List[Incidentbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
