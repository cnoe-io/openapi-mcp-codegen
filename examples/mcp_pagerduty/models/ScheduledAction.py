"""Model for ScheduledAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Scheduledaction(BaseModel):
    """Scheduledaction model"""

    type: str
    """The type of schedule action. Must be set to urgency_change."""
    at: Dict
    """Represents when scheduled action will occur."""
    to_urgency: str
    """Urgency level. Must be set to high."""

class ScheduledactionResponse(APIResponse):
    """Response model for Scheduledaction"""
    data: Optional[Scheduledaction] = None

class ScheduledactionListResponse(APIResponse):
    """List response model for Scheduledaction"""
    data: List[Scheduledaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
