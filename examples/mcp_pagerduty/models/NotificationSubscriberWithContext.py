"""Model for NotificationSubscriberWithContext"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationsubscriberwithcontext(BaseModel):
    """A reference of a subscriber entity with additional subscription context."""

    subscriber_id: Optional[str] = None
    """The ID of the entity being subscribed"""
    subscriber_type: Optional[str] = None
    """The type of the entity being subscribed"""
    has_indirect_subscription: Optional[bool] = None
    """If this subcriber has an indirect subscription to this incident via another object"""
    subscribed_via: Optional[List[Dict]] = None

class NotificationsubscriberwithcontextResponse(APIResponse):
    """Response model for Notificationsubscriberwithcontext"""
    data: Optional[Notificationsubscriberwithcontext] = None

class NotificationsubscriberwithcontextListResponse(APIResponse):
    """List response model for Notificationsubscriberwithcontext"""
    data: List[Notificationsubscriberwithcontext] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
