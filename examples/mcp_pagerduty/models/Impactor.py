"""Model for Impactor"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Impactor(BaseModel):
    """Impactor model"""

    id: Optional[str] = None
    type: Optional[str] = None
    """The kind of object that is impacting"""

class ImpactorResponse(APIResponse):
    """Response model for Impactor"""
    data: Optional[Impactor] = None

class ImpactorListResponse(APIResponse):
    """List response model for Impactor"""
    data: List[Impactor] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
