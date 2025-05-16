"""Model for UserRole"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Userrole(BaseModel):
    """Userrole model"""

    role: Optional[str] = None
    """The role of the user for a set of resources."""
    resources: Optional[List[str]] = None

class UserroleResponse(APIResponse):
    """Response model for Userrole"""
    data: Optional[Userrole] = None

class UserroleListResponse(APIResponse):
    """List response model for Userrole"""
    data: List[Userrole] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
