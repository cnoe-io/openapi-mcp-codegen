"""Model for StatusDashboard"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statusdashboard(BaseModel):
    """Statusdashboard model"""

    id: Optional[str] = None
    url_slug: Optional[str] = None
    name: Optional[str] = None

class StatusdashboardResponse(APIResponse):
    """Response model for Statusdashboard"""
    data: Optional[Statusdashboard] = None

class StatusdashboardListResponse(APIResponse):
    """List response model for Statusdashboard"""
    data: List[Statusdashboard] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
