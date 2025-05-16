"""Model for WeeklyRestriction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Weeklyrestriction(BaseModel):
    """Weeklyrestriction model"""


class WeeklyrestrictionResponse(APIResponse):
    """Response model for Weeklyrestriction"""
    data: Optional[Weeklyrestriction] = None

class WeeklyrestrictionListResponse(APIResponse):
    """List response model for Weeklyrestriction"""
    data: List[Weeklyrestriction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
