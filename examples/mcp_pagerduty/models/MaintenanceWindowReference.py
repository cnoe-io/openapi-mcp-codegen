"""Model for MaintenanceWindowReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Maintenancewindowreference(BaseModel):
    """Maintenancewindowreference model"""


class MaintenancewindowreferenceResponse(APIResponse):
    """Response model for Maintenancewindowreference"""
    data: Optional[Maintenancewindowreference] = None

class MaintenancewindowreferenceListResponse(APIResponse):
    """List response model for Maintenancewindowreference"""
    data: List[Maintenancewindowreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
