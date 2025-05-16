"""Model for NotificationSubscribable"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationsubscribable(BaseModel):
    """A reference of a subscribable entity."""

    subscribable_id: Optional[str] = None
    """The ID of the entity to subscribe to"""
    subscribable_type: Optional[str] = None
    """The type of the entity being subscribed to"""

class NotificationsubscribableResponse(APIResponse):
    """Response model for Notificationsubscribable"""
    data: Optional[Notificationsubscribable] = None

class NotificationsubscribableListResponse(APIResponse):
    """List response model for Notificationsubscribable"""
    data: List[Notificationsubscribable] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
