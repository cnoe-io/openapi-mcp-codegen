"""Model for AutomationActionsAbstractActionPostBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsabstractactionpostbody(BaseModel):
    """Automationactionsabstractactionpostbody model"""

    name: str
    description: str
    action_classification: Optional[str] = None
    action_type: str
    runner: Optional[str] = None
    services: Optional[List[str]] = None
    teams: Optional[List[str]] = None
    only_invocable_on_unresolved_incidents: Optional[bool] = None
    """If true, the action can only be invoked against an unresolved incident."""
    allow_invocation_manually: Optional[bool] = None
    """If true, the action can only be invoked manually by a user."""
    allow_invocation_from_event_orchestration: Optional[bool] = None
    """If true, the action can only be invoked automatically by an Event Orchestration."""
    map_to_all_services: Optional[bool] = None
    """If true, the action will be associated with every service."""

class AutomationactionsabstractactionpostbodyResponse(APIResponse):
    """Response model for Automationactionsabstractactionpostbody"""
    data: Optional[Automationactionsabstractactionpostbody] = None

class AutomationactionsabstractactionpostbodyListResponse(APIResponse):
    """List response model for Automationactionsabstractactionpostbody"""
    data: List[Automationactionsabstractactionpostbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
