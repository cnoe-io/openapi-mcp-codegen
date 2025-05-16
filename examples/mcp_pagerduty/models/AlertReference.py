"""Model for AlertReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertreference(BaseModel):
    """Alertreference model"""


class AlertreferenceResponse(APIResponse):
    """Response model for Alertreference"""
    data: Optional[Alertreference] = None

class AlertreferenceListResponse(APIResponse):
    """List response model for Alertreference"""
    data: List[Alertreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
