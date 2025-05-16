"""Model for StatusPagePostUpdate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostupdate(BaseModel):
    """An update for a Post."""

    id: Optional[str] = None
    """The ID of the Post Update."""
    self: Optional[str] = None
    """The path to which the Post Update resource is accessible."""
    post: Optional[Dict] = None
    """Status Page Post"""
    message: Optional[str] = None
    """The message of the Post Update."""
    reviewed_status: Optional[str] = None
    """The status of the Post Updates to retrieve."""
    status: Optional[Dict] = None
    """Status Page Status"""
    severity: Optional[Dict] = None
    """Status Page Severity"""
    impacted_services: Optional[List[Dict]] = None
    """Impacted services represent the status page services affected by a post update, and its impact."""
    update_frequency_ms: Optional[int] = None
    """The frequency of the next Post Update in milliseconds."""
    notify_subscribers: Optional[bool] = None
    """Determines if the subscribers should be notified of the Post Update."""
    reported_at: Optional[str] = None
    """The date and time the Post Update was reported."""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Post Update."""

class StatuspagepostupdateResponse(APIResponse):
    """Response model for Statuspagepostupdate"""
    data: Optional[Statuspagepostupdate] = None

class StatuspagepostupdateListResponse(APIResponse):
    """List response model for Statuspagepostupdate"""
    data: List[Statuspagepostupdate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
