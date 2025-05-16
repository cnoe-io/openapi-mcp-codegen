"""Model for StatusPageService"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspageservice(BaseModel):
    """A Service represents a PagerDuty service that is linked to a Status Page."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a Service entry."""
    self: Optional[str] = None
    """The API resource URL of the Service."""
    name: Optional[str] = None
    """The name of the Service."""
    status_page: Optional[Dict] = None
    """Status Page"""
    business_service: Optional[str] = None
    """Business Service"""
    type: Optional[str] = None
    """A string that determines the schema of the object."""

class StatuspageserviceResponse(APIResponse):
    """Response model for Statuspageservice"""
    data: Optional[Statuspageservice] = None

class StatuspageserviceListResponse(APIResponse):
    """List response model for Statuspageservice"""
    data: List[Statuspageservice] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
