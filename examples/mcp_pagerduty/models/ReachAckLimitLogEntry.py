"""Model for ReachAckLimitLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Reachacklimitlogentry(BaseModel):
    """Reachacklimitlogentry model"""


class ReachacklimitlogentryResponse(APIResponse):
    """Response model for Reachacklimitlogentry"""
    data: Optional[Reachacklimitlogentry] = None

class ReachacklimitlogentryListResponse(APIResponse):
    """List response model for Reachacklimitlogentry"""
    data: List[Reachacklimitlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
