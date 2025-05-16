"""Model for NotifyLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notifylogentry(BaseModel):
    """Notifylogentry model"""


class NotifylogentryResponse(APIResponse):
    """Response model for Notifylogentry"""
    data: Optional[Notifylogentry] = None

class NotifylogentryListResponse(APIResponse):
    """List response model for Notifylogentry"""
    data: List[Notifylogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
