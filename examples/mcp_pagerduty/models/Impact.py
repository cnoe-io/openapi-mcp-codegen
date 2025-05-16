"""Model for Impact"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Impact(BaseModel):
    """Impact model"""

    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    """The kind of object that has been impacted"""
    status: Optional[str] = None
    """The current impact status of the object"""
    additional_fields: Optional[Dict] = None

class ImpactResponse(APIResponse):
    """Response model for Impact"""
    data: Optional[Impact] = None

class ImpactListResponse(APIResponse):
    """List response model for Impact"""
    data: List[Impact] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
