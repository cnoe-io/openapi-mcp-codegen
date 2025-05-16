"""Model for StandardApplied"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Standardapplied(BaseModel):
    """Standardapplied model"""

    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    score: Optional[Dict] = None
    standards: Optional[List[Dict]] = None

class StandardappliedResponse(APIResponse):
    """Response model for Standardapplied"""
    data: Optional[Standardapplied] = None

class StandardappliedListResponse(APIResponse):
    """List response model for Standardapplied"""
    data: List[Standardapplied] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
