"""Model for StatusPagePostmortemRequest"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostmortemrequest(BaseModel):
    """Request to create/update a given Postmortem resource."""

    type: str
    """The type of the object returned by the API - in this case, a Status Page Post Postmortem."""
    post: Dict
    """Status Page Post"""
    message: str
    """The message of the Postmortem (supports Rich-Text)."""
    notify_subscribers: bool
    """Whether or not subscribers of the Status Page should be notified about the Postmortem."""

class StatuspagepostmortemrequestResponse(APIResponse):
    """Response model for Statuspagepostmortemrequest"""
    data: Optional[Statuspagepostmortemrequest] = None

class StatuspagepostmortemrequestListResponse(APIResponse):
    """List response model for Statuspagepostmortemrequest"""
    data: List[Statuspagepostmortemrequest] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
