"""Model for Alert"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alert(BaseModel):
    """Alert model"""


class AlertResponse(APIResponse):
    """Response model for Alert"""
    data: Optional[Alert] = None

class AlertListResponse(APIResponse):
    """List response model for Alert"""
    data: List[Alert] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
