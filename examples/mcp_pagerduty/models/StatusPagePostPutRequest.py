"""Model for StatusPagePostPutRequest"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostputrequest(BaseModel):
    """Request schema for creating a given Status Page Post resource."""

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
    status_page: Dict
    """Status Page"""

class StatuspagepostputrequestResponse(APIResponse):
    """Response model for Statuspagepostputrequest"""
    data: Optional[Statuspagepostputrequest] = None

class StatuspagepostputrequestListResponse(APIResponse):
    """List response model for Statuspagepostputrequest"""
    data: List[Statuspagepostputrequest] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
