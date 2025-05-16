"""Model for Schedule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Schedule(BaseModel):
    """Schedule model"""


class ScheduleResponse(APIResponse):
    """Response model for Schedule"""
    data: Optional[Schedule] = None

class ScheduleListResponse(APIResponse):
    """List response model for Schedule"""
    data: List[Schedule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
