"""Model for ChangeEvent"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Changeevent(BaseModel):
    """Changeevent model"""


class ChangeeventResponse(APIResponse):
    """Response model for Changeevent"""
    data: Optional[Changeevent] = None

class ChangeeventListResponse(APIResponse):
    """List response model for Changeevent"""
    data: List[Changeevent] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
