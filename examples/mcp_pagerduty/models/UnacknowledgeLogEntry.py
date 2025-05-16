"""Model for UnacknowledgeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Unacknowledgelogentry(BaseModel):
    """Unacknowledgelogentry model"""


class UnacknowledgelogentryResponse(APIResponse):
    """Response model for Unacknowledgelogentry"""
    data: Optional[Unacknowledgelogentry] = None

class UnacknowledgelogentryListResponse(APIResponse):
    """List response model for Unacknowledgelogentry"""
    data: List[Unacknowledgelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
