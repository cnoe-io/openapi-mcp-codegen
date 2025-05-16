"""Model for WebhooksV1AssignedToUser"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksv1assignedtouser(BaseModel):
    """The user assigned to the incident."""

    id: Optional[str] = None
    name: Optional[str] = None
    """The user's name."""
    email: Optional[str] = None
    """The user's email address."""
    html_url: Optional[str] = None

class Webhooksv1assignedtouserResponse(APIResponse):
    """Response model for Webhooksv1assignedtouser"""
    data: Optional[Webhooksv1assignedtouser] = None

class Webhooksv1assignedtouserListResponse(APIResponse):
    """List response model for Webhooksv1assignedtouser"""
    data: List[Webhooksv1assignedtouser] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
