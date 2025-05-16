"""Model for StatusPageSubscription"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statuspagesubscription(BaseModel):
    """A StatusPageSubscription resource represents a subscription to a specific status page entity."""

    channel: Optional[str] = None
    """The channel of the subscription."""
    contact: Optional[str] = None
    """The subscriber's contact - email address, webhook URL, etc..."""
    id: Optional[str] = None
    """The ID of the Subscription."""
    self: Optional[str] = None
    """The path in which the Subscription resource is accessible."""
    status: Optional[str] = None
    """The status of the Subscription."""
    status_page: Optional[Dict] = None
    """Status Page"""
    subscribable_object: Optional[Dict] = None
    """The subscribed entity for a given subscription."""
    type: Optional[str] = None
    """A string that determines the schema of the object."""

class StatuspagesubscriptionResponse(APIResponse):
    """Response model for Statuspagesubscription"""
    data: Optional[Statuspagesubscription] = None

class StatuspagesubscriptionListResponse(APIResponse):
    """List response model for Statuspagesubscription"""
    data: List[Statuspagesubscription] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
