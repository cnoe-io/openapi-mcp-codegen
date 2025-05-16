"""Model for LiveListResponse"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Livelistresponse(BaseModel):
    """Livelistresponse model"""

    limit: Optional[int] = None
    """Echoes limit pagination property."""
    more: Optional[bool] = None
    """Indicates if there are additional records to return"""

class LivelistresponseResponse(APIResponse):
    """Response model for Livelistresponse"""
    data: Optional[Livelistresponse] = None

class LivelistresponseListResponse(APIResponse):
    """List response model for Livelistresponse"""
    data: List[Livelistresponse] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
