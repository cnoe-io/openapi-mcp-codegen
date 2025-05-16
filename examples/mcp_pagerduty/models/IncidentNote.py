"""Model for IncidentNote"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentnote(BaseModel):
    """Incidentnote model"""

    id: Optional[str] = None
    user: Optional[str] = None
    channel: Optional[Dict] = None
    """The means by which this Note was created. Has different formats depending on type."""
    content: str
    """The note content"""
    created_at: Optional[str] = None
    """The time at which the note was submitted"""

class IncidentnoteResponse(APIResponse):
    """Response model for Incidentnote"""
    data: Optional[Incidentnote] = None

class IncidentnoteListResponse(APIResponse):
    """List response model for Incidentnote"""
    data: List[Incidentnote] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
