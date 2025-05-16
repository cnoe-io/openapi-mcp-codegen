"""Model for MaintenanceWindow"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Maintenancewindow(BaseModel):
    """Maintenancewindow model"""


class MaintenancewindowResponse(APIResponse):
    """Response model for Maintenancewindow"""
    data: Optional[Maintenancewindow] = None

class MaintenancewindowListResponse(APIResponse):
    """List response model for Maintenancewindow"""
    data: List[Maintenancewindow] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
