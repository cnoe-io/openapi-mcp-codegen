"""Model for WebhooksV1Message"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhooksv1message(BaseModel):
    """A message containing information about a single PagerDuty action."""

    id: Optional[str] = None
    """Uniquely identifies this outgoing webhook message; can be used for idempotency when processing the messages."""
    type: Optional[str] = None
    """The type of action being reported by this message."""
    created_on: Optional[str] = None
    """The date/time when the incident changed state."""
    data: Optional[Dict] = None

class Webhooksv1messageResponse(APIResponse):
    """Response model for Webhooksv1message"""
    data: Optional[Webhooksv1message] = None

class Webhooksv1messageListResponse(APIResponse):
    """List response model for Webhooksv1message"""
    data: List[Webhooksv1message] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
