"""Model for StatusPageSeverity"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspageseverity(BaseModel):
    """A Severity represents a level of impact for a given Status Page post."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a Severity entry."""
    self: Optional[str] = None
    """The API resource URL of the Severity."""
    description: Optional[str] = None
    """The description is a human-readable text that describes the Severity level."""
    post_type: Optional[str] = None
    """The type of the Post."""
    status_page: Optional[Dict] = None
    """Status Page"""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Severity."""

class StatuspageseverityResponse(APIResponse):
    """Response model for Statuspageseverity"""
    data: Optional[Statuspageseverity] = None

class StatuspageseverityListResponse(APIResponse):
    """List response model for Statuspageseverity"""
    data: List[Statuspageseverity] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
