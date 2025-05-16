"""Model for ServiceReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicereference(BaseModel):
    """Servicereference model"""


class ServicereferenceResponse(APIResponse):
    """Response model for Servicereference"""
    data: Optional[Servicereference] = None

class ServicereferenceListResponse(APIResponse):
    """List response model for Servicereference"""
    data: List[Servicereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
