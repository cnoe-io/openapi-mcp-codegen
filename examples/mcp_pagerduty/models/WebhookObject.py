"""Model for WebhookObject"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhookobject(BaseModel):
    """Webhookobject model"""


class WebhookobjectResponse(APIResponse):
    """Response model for Webhookobject"""
    data: Optional[Webhookobject] = None

class WebhookobjectListResponse(APIResponse):
    """List response model for Webhookobject"""
    data: List[Webhookobject] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
