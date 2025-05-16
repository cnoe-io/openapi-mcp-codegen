"""Model for Addon"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Addon(BaseModel):
    """Addon model"""


class AddonResponse(APIResponse):
    """Response model for Addon"""
    data: Optional[Addon] = None

class AddonListResponse(APIResponse):
    """List response model for Addon"""
    data: List[Addon] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
