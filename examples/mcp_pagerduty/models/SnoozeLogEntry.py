"""Model for SnoozeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Snoozelogentry(BaseModel):
    """Snoozelogentry model"""


class SnoozelogentryResponse(APIResponse):
    """Response model for Snoozelogentry"""
    data: Optional[Snoozelogentry] = None

class SnoozelogentryListResponse(APIResponse):
    """List response model for Snoozelogentry"""
    data: List[Snoozelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
