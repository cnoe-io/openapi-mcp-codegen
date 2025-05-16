"""Model for ExhaustEscalationPathLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Exhaustescalationpathlogentry(BaseModel):
    """Exhaustescalationpathlogentry model"""


class ExhaustescalationpathlogentryResponse(APIResponse):
    """Response model for Exhaustescalationpathlogentry"""
    data: Optional[Exhaustescalationpathlogentry] = None

class ExhaustescalationpathlogentryListResponse(APIResponse):
    """List response model for Exhaustescalationpathlogentry"""
    data: List[Exhaustescalationpathlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
