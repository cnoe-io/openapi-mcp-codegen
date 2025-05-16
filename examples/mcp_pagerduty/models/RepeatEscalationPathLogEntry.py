"""Model for RepeatEscalationPathLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Repeatescalationpathlogentry(BaseModel):
    """Repeatescalationpathlogentry model"""


class RepeatescalationpathlogentryResponse(APIResponse):
    """Response model for Repeatescalationpathlogentry"""
    data: Optional[Repeatescalationpathlogentry] = None

class RepeatescalationpathlogentryListResponse(APIResponse):
    """List response model for Repeatescalationpathlogentry"""
    data: List[Repeatescalationpathlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
