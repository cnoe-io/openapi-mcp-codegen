"""Model for WebhookSubscription"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksubscription(BaseModel):
    """Webhooksubscription model"""

    id: Optional[str] = None
    type: str
    """The type indicating the schema of the object."""
    active: Optional[bool] = None
    """Determines whether this subscription will produce webhook events."""
    delivery_method: Dict
    description: Optional[str] = None
    """A short description of the webhook subscription."""
    events: List[str]
    """The set of outbound event types the webhook will receive."""
    filter: Dict

class WebhooksubscriptionResponse(APIResponse):
    """Response model for Webhooksubscription"""
    data: Optional[Webhooksubscription] = None

class WebhooksubscriptionListResponse(APIResponse):
    """List response model for Webhooksubscription"""
    data: List[Webhooksubscription] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
