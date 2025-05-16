"""Model for ResolveReason"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Resolvereason(BaseModel):
    """Resolvereason model"""

    type: Optional[str] = None
    """The reason the incident was resolved. The only reason currently supported is merge."""
    incident: Optional[str] = None

class ResolvereasonResponse(APIResponse):
    """Response model for Resolvereason"""
    data: Optional[Resolvereason] = None

class ResolvereasonListResponse(APIResponse):
    """List response model for Resolvereason"""
    data: List[Resolvereason] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
