"""Model for Webhook"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhook(BaseModel):
    """Information about the configured webhook."""

    endpoint_url: Optional[str] = None
    """The url endpoint the webhook payload is sent to."""
    name: Optional[str] = None
    """The name of the webhook."""
    webhook_object: Optional[str] = None
    config: Optional[Dict] = None
    """The object that contains webhook configuration values depending on the webhook type specification."""
    outbound_integration: Optional[str] = None

class WebhookResponse(APIResponse):
    """Response model for Webhook"""
    data: Optional[Webhook] = None

class WebhookListResponse(APIResponse):
    """List response model for Webhook"""
    data: List[Webhook] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
