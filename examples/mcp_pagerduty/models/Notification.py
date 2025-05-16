"""Model for Notification"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notification(BaseModel):
    """Notification model"""

    id: Optional[str] = None
    type: Optional[str] = None
    """The type of notification."""
    started_at: Optional[str] = None
    """The time at which the notification was sent"""
    address: Optional[str] = None
    """The address where the notification was sent. This will be null for notification type `push_notification`."""
    user: Optional[str] = None
    conferenceAddress: Optional[str] = None
    """The address of the conference bridge"""
    status: Optional[str] = None
    : Optional[str] = None

class NotificationResponse(APIResponse):
    """Response model for Notification"""
    data: Optional[Notification] = None

class NotificationListResponse(APIResponse):
    """List response model for Notification"""
    data: List[Notification] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
