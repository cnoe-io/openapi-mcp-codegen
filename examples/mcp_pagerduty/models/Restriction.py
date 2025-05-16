"""Model for Restriction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Restriction(BaseModel):
    """Restriction model"""

    type: str
    """Specify the types of `restriction`."""
    duration_seconds: int
    """The duration of the restriction in seconds."""
    start_time_of_day: str
    """The start time in HH:mm:ss format."""
    start_day_of_week: Optional[int] = None
    """Only required for use with a `weekly_restriction` restriction type. The first day of the weekly rotation schedule as [ISO 8601 day](https://en.wikipedia.org/wiki/ISO_week_date) (1 is Monday, etc.)"""

class RestrictionResponse(APIResponse):
    """Response model for Restriction"""
    data: Optional[Restriction] = None

class RestrictionListResponse(APIResponse):
    """List response model for Restriction"""
    data: List[Restriction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
