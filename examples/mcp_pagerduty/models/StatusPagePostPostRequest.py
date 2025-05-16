"""Model for StatusPagePostPostRequest"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostpostrequest(BaseModel):
    """Request schema for creating/updating a given Status Page Post resource."""

    type: str
    """The type of the object returned by the API - in this case, a Status Page Post."""
    title: str
    """The title given to a Post."""
    post_type: str
    """The type of the Post."""
    starts_at: str
    """The date and time the Post intent becomes effective - only for maintenance post type."""
    ends_at: str
    """The date and time the Post intent is concluded - only for maintenance post type."""
    updates: List[str]
    """Post Updates to be associated with a Post"""
    status_page: Dict
    """Status Page"""

class StatuspagepostpostrequestResponse(APIResponse):
    """Response model for Statuspagepostpostrequest"""
    data: Optional[Statuspagepostpostrequest] = None

class StatuspagepostpostrequestListResponse(APIResponse):
    """List response model for Statuspagepostpostrequest"""
    data: List[Statuspagepostpostrequest] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
