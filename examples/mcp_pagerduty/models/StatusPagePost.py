"""Model for StatusPagePost"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagepost(BaseModel):
    """A Post represents a communication resource presented in the Status Page about certain aspects of one or more services associated."""

    id: Optional[str] = None
    """An unique identifier within Status Page scope that defines a single Post resource."""
    self: Optional[str] = None
    """The API resource URL of the Post."""
    type: Optional[str] = None
    """The type of the object returned by the API - in this case, a Status Page Post."""
    post_type: Optional[str] = None
    """The type of the Post."""
    status_page: Optional[Dict] = None
    """Status Page"""
    linked_resource: Optional[Dict] = None
    """Linked resource"""
    postmortem: Optional[Dict] = None
    """Postmortem"""
    title: Optional[str] = None
    """The title given to a Post."""
    starts_at: Optional[str] = None
    """The date and time the Post intent becomes effective - only for maintenance post type."""
    ends_at: Optional[str] = None
    """The date and time the Post intent is concluded - only for maintenance post type."""
    updates: Optional[List[Dict]] = None
    """List of status_page_post_update references associated to a Post."""

class StatuspagepostResponse(APIResponse):
    """Response model for Statuspagepost"""
    data: Optional[Statuspagepost] = None

class StatuspagepostListResponse(APIResponse):
    """List response model for Statuspagepost"""
    data: List[Statuspagepost] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
