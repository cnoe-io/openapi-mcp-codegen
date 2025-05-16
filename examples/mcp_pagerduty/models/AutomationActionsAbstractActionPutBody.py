"""Model for AutomationActionsAbstractActionPutBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsabstractactionputbody(BaseModel):
    """Automationactionsabstractactionputbody model"""

    name: Optional[str] = None
    description: Optional[str] = None
    action_classification: Optional[str] = None
    action_type: Optional[str] = None
    runner: Optional[str] = None
    only_invocable_on_unresolved_incidents: Optional[bool] = None
    """If true, the action can only be invoked against an unresolved incident."""
    allow_invocation_manually: Optional[bool] = None
    """If true, the action can only be invoked manually by a user."""
    allow_invocation_from_event_orchestration: Optional[bool] = None
    """If true, the action can only be invoked automatically by an Event Orchestration."""
    map_to_all_services: Optional[bool] = None
    """If true, the action will be associated with every service."""

class AutomationactionsabstractactionputbodyResponse(APIResponse):
    """Response model for Automationactionsabstractactionputbody"""
    data: Optional[Automationactionsabstractactionputbody] = None

class AutomationactionsabstractactionputbodyListResponse(APIResponse):
    """List response model for Automationactionsabstractactionputbody"""
    data: List[Automationactionsabstractactionputbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
