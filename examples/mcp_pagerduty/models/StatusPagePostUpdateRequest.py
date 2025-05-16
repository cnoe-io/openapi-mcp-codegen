"""Model for StatusPagePostUpdateRequest"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostupdaterequest(BaseModel):
    """Attributes for Post Update creation/update"""

    self: Optional[str] = None
    """The path to which the Post Update resource is accessible."""
    post: Dict
    """Status Page Post"""
    message: str
    """The message of the Post Update."""
    status: Dict
    """Status Page Status"""
    severity: Dict
    """Status Page Severity"""
    impacted_services: List[str]
    """Impacted services represent the status page services affected by a post update, and its impact."""
    update_frequency_ms: int
    """The frequency of the next Post Update in milliseconds."""
    notify_subscribers: bool
    """Determines if the subscribers should be notified of the Post Update."""
    reported_at: Optional[str] = None
    """The date and time the Post Update was reported."""
    type: str
    """The type of the object returned by the API - in this case, a Status Page Post Update."""

class StatuspagepostupdaterequestResponse(APIResponse):
    """Response model for Statuspagepostupdaterequest"""
    data: Optional[Statuspagepostupdaterequest] = None

class StatuspagepostupdaterequestListResponse(APIResponse):
    """List response model for Statuspagepostupdaterequest"""
    data: List[Statuspagepostupdaterequest] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
