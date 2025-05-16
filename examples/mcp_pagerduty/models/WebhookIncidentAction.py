"""Model for WebhookIncidentAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhookincidentaction(BaseModel):
    """Webhookincidentaction model"""


class WebhookincidentactionResponse(APIResponse):
    """Response model for Webhookincidentaction"""
    data: Optional[Webhookincidentaction] = None

class WebhookincidentactionListResponse(APIResponse):
    """List response model for Webhookincidentaction"""
    data: List[Webhookincidentaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
