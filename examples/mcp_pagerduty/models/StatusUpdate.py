"""Model for StatusUpdate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statusupdate(BaseModel):
    """Statusupdate model"""

    id: Optional[str] = None
    message: Optional[str] = None
    """The message of the status update."""
    created_at: Optional[str] = None
    """The date/time when this status update was created."""
    sender: Optional[str] = None
    subject: Optional[str] = None
    """The subject of the custom html email status update. Present if included in request body."""
    html_message: Optional[str] = None
    """The html content of the custom html email status update. Present if included in request body."""

class StatusupdateResponse(APIResponse):
    """Response model for Statusupdate"""
    data: Optional[Statusupdate] = None

class StatusupdateListResponse(APIResponse):
    """List response model for Statusupdate"""
    data: List[Statusupdate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
