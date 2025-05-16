"""Model for EventRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Eventrule(BaseModel):
    """Eventrule model"""


class EventruleResponse(APIResponse):
    """Response model for Eventrule"""
    data: Optional[Eventrule] = None

class EventruleListResponse(APIResponse):
    """List response model for Eventrule"""
    data: List[Eventrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
