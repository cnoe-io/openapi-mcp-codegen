"""Model for StatusPageStatus"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagestatus(BaseModel):
    """A Status represents a level of undergoing work and/or assessment for a given Status Page post."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a Status entry."""
    self: Optional[str] = None
    """The API resource URL of the Status."""
    description: Optional[str] = None
    """The description is a human-readable text that describes the Status level."""
    post_type: Optional[str] = None
    """The type of the Post."""
    status_page: Optional[Dict] = None
    """Status Page"""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Status."""

class StatuspagestatusResponse(APIResponse):
    """Response model for Statuspagestatus"""
    data: Optional[Statuspagestatus] = None

class StatuspagestatusListResponse(APIResponse):
    """List response model for Statuspagestatus"""
    data: List[Statuspagestatus] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
