"""Model for AlertCount"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertcount(BaseModel):
    """Alertcount model"""

    triggered: Optional[int] = None
    """The count of triggered alerts grouped into this incident"""
    resolved: Optional[int] = None
    """The count of resolved alerts grouped into this incident"""
    all: Optional[int] = None
    """The total count of alerts grouped into this incident"""

class AlertcountResponse(APIResponse):
    """Response model for Alertcount"""
    data: Optional[Alertcount] = None

class AlertcountListResponse(APIResponse):
    """List response model for Alertcount"""
    data: List[Alertcount] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
