"""Model for Priority"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Priority(BaseModel):
    """Priority model"""


class PriorityResponse(APIResponse):
    """Response model for Priority"""
    data: Optional[Priority] = None

class PriorityListResponse(APIResponse):
    """List response model for Priority"""
    data: List[Priority] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
