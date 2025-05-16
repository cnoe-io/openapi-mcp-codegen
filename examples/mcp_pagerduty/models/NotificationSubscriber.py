"""Model for NotificationSubscriber"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationsubscriber(BaseModel):
    """A reference of a subscriber entity."""

    subscriber_id: Optional[str] = None
    """The ID of the entity being subscribed"""
    subscriber_type: Optional[str] = None
    """The type of the entity being subscribed"""

class NotificationsubscriberResponse(APIResponse):
    """Response model for Notificationsubscriber"""
    data: Optional[Notificationsubscriber] = None

class NotificationsubscriberListResponse(APIResponse):
    """List response model for Notificationsubscriber"""
    data: List[Notificationsubscriber] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
