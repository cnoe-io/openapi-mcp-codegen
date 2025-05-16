"""Model for HandoffNotificationRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Handoffnotificationrule(BaseModel):
    """A rule for contacting the user for Handoff Notifications."""

    id: str
    notify_advance_in_minutes: Optional[int] = None
    """The delay before firing the rule, in minutes."""
    handoff_type: str
    """The type of handoff being created."""
    contact_method: str

class HandoffnotificationruleResponse(APIResponse):
    """Response model for Handoffnotificationrule"""
    data: Optional[Handoffnotificationrule] = None

class HandoffnotificationruleListResponse(APIResponse):
    """List response model for Handoffnotificationrule"""
    data: List[Handoffnotificationrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
