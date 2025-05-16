"""Model for StatusPage"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspage(BaseModel):
    """A Status Page with all the configuration needed to present the system status in a public or private manner."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a Status Page entry."""
    name: Optional[str] = None
    """The name of a Status Page to be presented as a brand title (for example, the rendered Status Page HTML header)."""
    published_at: Optional[str] = None
    """The date time moment when a Status Page was published to be publicly available."""
    status_page_type: Optional[str] = None
    """The type of Status Pages to retrieve - public is accessible to everyone on the internet or private requiring some sort of authentication/authorization layer."""
    url: Optional[str] = None
    """The URL from which the Status Page can be accessed on the internet (either customer's domain or default *.trust.pagerduty.com)."""
    type: Optional[str] = None
    """A string that determines the schema of the object. This must be the standard name for the entity, suffixed by _reference if the object is a reference."""

class StatuspageResponse(APIResponse):
    """Response model for Statuspage"""
    data: Optional[Statuspage] = None

class StatuspageListResponse(APIResponse):
    """List response model for Statuspage"""
    data: List[Statuspage] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
