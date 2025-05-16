"""Model for LogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Logentry(BaseModel):
    """Logentry model"""


class LogentryResponse(APIResponse):
    """Response model for Logentry"""
    data: Optional[Logentry] = None

class LogentryListResponse(APIResponse):
    """List response model for Logentry"""
    data: List[Logentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
