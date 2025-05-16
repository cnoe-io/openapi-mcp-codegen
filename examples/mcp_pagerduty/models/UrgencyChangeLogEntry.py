"""Model for UrgencyChangeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Urgencychangelogentry(BaseModel):
    """Urgencychangelogentry model"""


class UrgencychangelogentryResponse(APIResponse):
    """Response model for Urgencychangelogentry"""
    data: Optional[Urgencychangelogentry] = None

class UrgencychangelogentryListResponse(APIResponse):
    """List response model for Urgencychangelogentry"""
    data: List[Urgencychangelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
