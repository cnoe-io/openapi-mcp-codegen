"""Model for IncidentPrivilege"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentprivilege(BaseModel):
    """Incidentprivilege model"""

    role: Optional[str] = None
    permissions: Optional[List[str]] = None

class IncidentprivilegeResponse(APIResponse):
    """Response model for Incidentprivilege"""
    data: Optional[Incidentprivilege] = None

class IncidentprivilegeListResponse(APIResponse):
    """List response model for Incidentprivilege"""
    data: List[Incidentprivilege] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
