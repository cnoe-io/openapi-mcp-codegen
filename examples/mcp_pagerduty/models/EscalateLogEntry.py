"""Model for EscalateLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Escalatelogentry(BaseModel):
    """Escalatelogentry model"""


class EscalatelogentryResponse(APIResponse):
    """Response model for Escalatelogentry"""
    data: Optional[Escalatelogentry] = None

class EscalatelogentryListResponse(APIResponse):
    """List response model for Escalatelogentry"""
    data: List[Escalatelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
