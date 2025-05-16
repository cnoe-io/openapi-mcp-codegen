"""Model for ServiceEventRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Serviceeventrule(BaseModel):
    """Serviceeventrule model"""


class ServiceeventruleResponse(APIResponse):
    """Response model for Serviceeventrule"""
    data: Optional[Serviceeventrule] = None

class ServiceeventruleListResponse(APIResponse):
    """List response model for Serviceeventrule"""
    data: List[Serviceeventrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
