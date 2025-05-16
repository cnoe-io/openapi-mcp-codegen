"""Model for StandardInclusionExclusion"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Standardinclusionexclusion(BaseModel):
    """Standardinclusionexclusion model"""

    type: Optional[str] = None
    id: Optional[str] = None

class StandardinclusionexclusionResponse(APIResponse):
    """Response model for Standardinclusionexclusion"""
    data: Optional[Standardinclusionexclusion] = None

class StandardinclusionexclusionListResponse(APIResponse):
    """List response model for Standardinclusionexclusion"""
    data: List[Standardinclusionexclusion] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
