"""Model for StatusPagePostmortem"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepostmortem(BaseModel):
    """A Postmortem represents a communication resource presented in the Status Page about follow-up made to a certain Post."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a single Postmortem resource."""
    self: Optional[str] = None
    """The API resource URL of the Postmortem."""
    post: Optional[Dict] = None
    """Status Page Post"""
    message: Optional[str] = None
    """The message of the Postmortem (supports Rich-Text)."""
    notify_subscribers: Optional[bool] = None
    """Whether or not subscribers of the Status Page should be notified about the Postmortem."""
    reported_at: Optional[str] = None
    """The date and time the Postmortem was reported."""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Post Postmortem."""

class StatuspagepostmortemResponse(APIResponse):
    """Response model for Statuspagepostmortem"""
    data: Optional[Statuspagepostmortem] = None

class StatuspagepostmortemListResponse(APIResponse):
    """List response model for Statuspagepostmortem"""
    data: List[Statuspagepostmortem] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
