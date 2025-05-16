"""Model for WebhooksV1AssignedTo"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksv1assignedto(BaseModel):
    """Webhooksv1assignedto model"""

    at: Optional[str] = None
    """Time at which the assignment was created."""
    object: Optional[str] = None

class Webhooksv1assignedtoResponse(APIResponse):
    """Response model for Webhooksv1assignedto"""
    data: Optional[Webhooksv1assignedto] = None

class Webhooksv1assignedtoListResponse(APIResponse):
    """List response model for Webhooksv1assignedto"""
    data: List[Webhooksv1assignedto] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
