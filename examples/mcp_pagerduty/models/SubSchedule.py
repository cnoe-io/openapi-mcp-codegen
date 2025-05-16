"""Model for SubSchedule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Subschedule(BaseModel):
    """Subschedule model"""

    name: str
    """The name of the subschedule"""
    rendered_schedule_entries: Optional[List[str]] = None
    """This is a list of entries on the computed layer for the current time range. Since or until must be set in order for this field to be populated."""
    rendered_coverage_percentage: Optional[float] = None
    """The percentage of the time range covered by this layer. Returns null unless since or until are set."""

class SubscheduleResponse(APIResponse):
    """Response model for Subschedule"""
    data: Optional[Subschedule] = None

class SubscheduleListResponse(APIResponse):
    """List response model for Subschedule"""
    data: List[Subschedule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
