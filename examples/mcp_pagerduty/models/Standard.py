"""Model for Standard"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Standard(BaseModel):
    """Standard model"""

    active: Optional[bool] = None
    description: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    resource_type: Optional[str] = None
    exclusions: Optional[List[str]] = None
    inclusions: Optional[List[str]] = None

class StandardResponse(APIResponse):
    """Response model for Standard"""
    data: Optional[Standard] = None

class StandardListResponse(APIResponse):
    """List response model for Standard"""
    data: List[Standard] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
