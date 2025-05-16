"""Model for AssignLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Assignlogentry(BaseModel):
    """Assignlogentry model"""


class AssignlogentryResponse(APIResponse):
    """Response model for Assignlogentry"""
    data: Optional[Assignlogentry] = None

class AssignlogentryListResponse(APIResponse):
    """List response model for Assignlogentry"""
    data: List[Assignlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
