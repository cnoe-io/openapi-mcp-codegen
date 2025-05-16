"""Model for NotificationSubscription"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationsubscription(BaseModel):
    """An object describing the relationship of a NotificationSubscriber and a NotificationSubscribable."""

    subscriber_id: Optional[str] = None
    """The ID of the entity being subscribed"""
    subscriber_type: Optional[str] = None
    """The type of the entity being subscribed"""
    subscribable_id: Optional[str] = None
    """The ID of the entity being subscribed to"""
    subscribable_type: Optional[str] = None
    """The type of the entity being subscribed to"""
    account_id: Optional[str] = None
    """The ID of the account belonging to the subscriber entity"""

class NotificationsubscriptionResponse(APIResponse):
    """Response model for Notificationsubscription"""
    data: Optional[Notificationsubscription] = None

class NotificationsubscriptionListResponse(APIResponse):
    """List response model for Notificationsubscription"""
    data: List[Notificationsubscription] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
