"""Model for WebhookSubscriptionUpdate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksubscriptionupdate(BaseModel):
    """Webhooksubscriptionupdate model"""

    webhook_subscription: Optional[Dict] = None

class WebhooksubscriptionupdateResponse(APIResponse):
    """Response model for Webhooksubscriptionupdate"""
    data: Optional[Webhooksubscriptionupdate] = None

class WebhooksubscriptionupdateListResponse(APIResponse):
    """List response model for Webhooksubscriptionupdate"""
    data: List[Webhooksubscriptionupdate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
