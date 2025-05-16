"""Model for Override"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Override(BaseModel):
    """Override model"""


class OverrideResponse(APIResponse):
    """Response model for Override"""
    data: Optional[Override] = None

class OverrideListResponse(APIResponse):
    """List response model for Override"""
    data: List[Override] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
