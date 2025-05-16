"""Model for ScheduleLayerUser"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Schedulelayeruser(BaseModel):
    """Schedulelayeruser model"""

    user: str

class SchedulelayeruserResponse(APIResponse):
    """Response model for Schedulelayeruser"""
    data: Optional[Schedulelayeruser] = None

class SchedulelayeruserListResponse(APIResponse):
    """List response model for Schedulelayeruser"""
    data: List[Schedulelayeruser] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
