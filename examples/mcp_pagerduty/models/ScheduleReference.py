"""Model for ScheduleReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Schedulereference(BaseModel):
    """Schedulereference model"""


class SchedulereferenceResponse(APIResponse):
    """Response model for Schedulereference"""
    data: Optional[Schedulereference] = None

class SchedulereferenceListResponse(APIResponse):
    """List response model for Schedulereference"""
    data: List[Schedulereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
