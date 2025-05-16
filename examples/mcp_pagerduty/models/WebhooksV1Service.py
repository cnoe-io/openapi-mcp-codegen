"""Model for WebhooksV1Service"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksv1service(BaseModel):
    """The service on which the incident occurred."""

    id: Optional[str] = None
    name: Optional[str] = None
    """The name of the service."""
    html_url: Optional[str] = None
    deleted_at: Optional[str] = None
    """The date/time the service was deleted, if it has been removed."""
    description: Optional[str] = None
    """The description of the service."""

class Webhooksv1serviceResponse(APIResponse):
    """Response model for Webhooksv1service"""
    data: Optional[Webhooksv1service] = None

class Webhooksv1serviceListResponse(APIResponse):
    """List response model for Webhooksv1service"""
    data: List[Webhooksv1service] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
