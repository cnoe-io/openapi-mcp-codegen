"""Model for TriggerLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Triggerlogentry(BaseModel):
    """Triggerlogentry model"""


class TriggerlogentryResponse(APIResponse):
    """Response model for Triggerlogentry"""
    data: Optional[Triggerlogentry] = None

class TriggerlogentryListResponse(APIResponse):
    """List response model for Triggerlogentry"""
    data: List[Triggerlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
