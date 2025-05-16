"""Model for Action"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Action(BaseModel):
    """A message containing information about a single PagerDuty action."""

    id: Optional[str] = None
    """Uniquely identifies this outgoing webhook message; can be used for idempotency when processing the messages."""
    triggered_at: Optional[str] = None
    """The date/time when this message was was sent."""
    webhook: Optional[str] = None

class ActionResponse(APIResponse):
    """Response model for Action"""
    data: Optional[Action] = None

class ActionListResponse(APIResponse):
    """List response model for Action"""
    data: List[Action] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
