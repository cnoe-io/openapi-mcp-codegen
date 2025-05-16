"""Model for ScheduleLayerEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Schedulelayerentry(BaseModel):
    """Schedulelayerentry model"""

    user: Optional[str] = None
    start: str
    """The start time of this entry."""
    end: str
    """The end time of this entry. If null, the entry does not end."""

class SchedulelayerentryResponse(APIResponse):
    """Response model for Schedulelayerentry"""
    data: Optional[Schedulelayerentry] = None

class SchedulelayerentryListResponse(APIResponse):
    """List response model for Schedulelayerentry"""
    data: List[Schedulelayerentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
