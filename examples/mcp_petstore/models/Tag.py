"""Model for Tag"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Tag(BaseModel):
    """Tag model"""

    id: Optional[int] = None
    name: Optional[str] = None

class TagResponse(APIResponse):
    """Response model for Tag"""
    data: Optional[Tag] = None

class TagListResponse(APIResponse):
    """List response model for Tag"""
    data: List[Tag] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
