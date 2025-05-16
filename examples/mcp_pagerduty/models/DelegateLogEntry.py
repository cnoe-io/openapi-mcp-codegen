"""Model for DelegateLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Delegatelogentry(BaseModel):
    """Delegatelogentry model"""


class DelegatelogentryResponse(APIResponse):
    """Response model for Delegatelogentry"""
    data: Optional[Delegatelogentry] = None

class DelegatelogentryListResponse(APIResponse):
    """List response model for Delegatelogentry"""
    data: List[Delegatelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
