"""Model for ScheduleLayer"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Schedulelayer(BaseModel):
    """Schedulelayer model"""

    id: Optional[str] = None
    start: str
    """The start time of this layer."""
    end: Optional[str] = None
    """The end time of this layer. If `null`, the layer does not end."""
    users: List[str]
    """The ordered list of users on this layer. The position of the user on the list determines their order in the layer."""
    restrictions: Optional[List[str]] = None
    """An array of restrictions for the layer. A restriction is a limit on which period of the day or week the schedule layer can accept assignments. Restrictions respect the `time_zone` parameter of the request."""
    rotation_virtual_start: str
    """The effective start time of the layer. This can be before the start time of the schedule."""
    rotation_turn_length_seconds: int
    """The duration of each on-call shift in seconds."""
    name: Optional[str] = None
    """The name of the schedule layer."""
    rendered_schedule_entries: Optional[List[str]] = None
    """This is a list of entries on the computed layer for the current time range. Since or until must be set in order for this field to be populated."""
    rendered_coverage_percentage: Optional[float] = None
    """The percentage of the time range covered by this layer. Returns null unless since or until are set."""

class SchedulelayerResponse(APIResponse):
    """Response model for Schedulelayer"""
    data: Optional[Schedulelayer] = None

class SchedulelayerListResponse(APIResponse):
    """List response model for Schedulelayer"""
    data: List[Schedulelayer] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
