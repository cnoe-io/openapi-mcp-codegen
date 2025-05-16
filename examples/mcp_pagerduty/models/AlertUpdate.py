"""Model for AlertUpdate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertupdate(BaseModel):
    """Alertupdate model"""

    status: Optional[str] = None
    incident: Optional[str] = None

class AlertupdateResponse(APIResponse):
    """Response model for Alertupdate"""
    data: Optional[Alertupdate] = None

class AlertupdateListResponse(APIResponse):
    """List response model for Alertupdate"""
    data: List[Alertupdate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
