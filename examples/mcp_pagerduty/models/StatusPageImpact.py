"""Model for StatusPageImpact"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspageimpact(BaseModel):
    """A StatusPageImpact resource represents a level of impact for a given Status Page Post."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a Impact entry."""
    self: Optional[str] = None
    """The API resource URL of the Impact."""
    description: Optional[str] = None
    """The description is a human-readable text that describes the Impact level."""
    post_type: Optional[str] = None
    """The type of the Post."""
    status_page: Optional[Dict] = None
    """Status Page"""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Impact."""

class StatuspageimpactResponse(APIResponse):
    """Response model for Statuspageimpact"""
    data: Optional[Statuspageimpact] = None

class StatuspageimpactListResponse(APIResponse):
    """List response model for Statuspageimpact"""
    data: List[Statuspageimpact] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
