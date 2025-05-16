"""Model for SupportHours"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Supporthours(BaseModel):
    """Supporthours model"""

    type: Optional[str] = None
    """The type of support hours"""
    time_zone: Optional[str] = None
    """The time zone for the support hours"""
    days_of_week: Optional[List[int]] = None
    start_time: Optional[str] = None
    """The support hours' starting time of day (date portion is ignored)"""
    end_time: Optional[str] = None
    """The support hours' ending time of day (date portion is ignored)"""

class SupporthoursResponse(APIResponse):
    """Response model for Supporthours"""
    data: Optional[Supporthours] = None

class SupporthoursListResponse(APIResponse):
    """List response model for Supporthours"""
    data: List[Supporthours] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
