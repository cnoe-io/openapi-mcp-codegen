"""Model for Service"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Service(BaseModel):
    """Service model"""


class ServiceResponse(APIResponse):
    """Response model for Service"""
    data: Optional[Service] = None

class ServiceListResponse(APIResponse):
    """List response model for Service"""
    data: List[Service] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
