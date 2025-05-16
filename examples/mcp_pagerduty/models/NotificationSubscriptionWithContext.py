"""Model for NotificationSubscriptionWithContext"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationsubscriptionwithcontext(BaseModel):
    """An object describing the relationship of a NotificationSubscriber and a NotificationSubscribable with additional context on status of subscription attempt."""

    subscriber_id: Optional[str] = None
    """The ID of the entity being subscribed"""
    subscriber_type: Optional[str] = None
    """The type of the entity being subscribed"""
    subscribable_id: Optional[str] = None
    """The ID of the entity being subscribed to"""
    subscribable_type: Optional[str] = None
    """The type of the entity being subscribed to"""
    account_id: Optional[str] = None
    """The type of the entity being subscribed to"""
    result: Optional[str] = None
    """The resulting status of the subscription"""

class NotificationsubscriptionwithcontextResponse(APIResponse):
    """Response model for Notificationsubscriptionwithcontext"""
    data: Optional[Notificationsubscriptionwithcontext] = None

class NotificationsubscriptionwithcontextListResponse(APIResponse):
    """List response model for Notificationsubscriptionwithcontext"""
    data: List[Notificationsubscriptionwithcontext] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
