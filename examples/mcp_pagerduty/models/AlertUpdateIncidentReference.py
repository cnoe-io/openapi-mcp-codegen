"""Model for AlertUpdateIncidentReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertupdateincidentreference(BaseModel):
    """Alertupdateincidentreference model"""

    id: str
    type: Optional[str] = None

class AlertupdateincidentreferenceResponse(APIResponse):
    """Response model for Alertupdateincidentreference"""
    data: Optional[Alertupdateincidentreference] = None

class AlertupdateincidentreferenceListResponse(APIResponse):
    """List response model for Alertupdateincidentreference"""
    data: List[Alertupdateincidentreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
