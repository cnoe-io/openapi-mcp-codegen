"""Model for EventRuleActionsCommon"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Eventruleactionscommon(BaseModel):
    """When an event matches this Event Rule, the actions that will be taken to change the resulting Alert and Incident."""

    annotate: Optional[Dict] = None
    """Set a note on the resulting incident."""
    event_action: Optional[Dict] = None
    """Set whether the resulting alert status is trigger or resolve."""
    extractions: Optional[List[str]] = None
    """Dynamically extract values to set and modify new and existing PD-CEF fields."""
    priority: Optional[Dict] = None
    """Set the priority ID for the resulting incident. You can find the priority you want by calling the priorities endpoint."""
    severity: Optional[Dict] = None
    """Set the severity of the resulting alert."""
    suppress: Optional[Dict] = None
    """Set whether the resulting alert is suppressed. Can optionally be used with a threshold where resulting alerts will be suppressed until the threshold is met in a window of time. If using a threshold the rule must also set a route action."""
    suspend: Optional[Dict] = None
    """Set the length of time to suspend the resulting alert before triggering. Rules with a suspend action must also set a route action, and cannot have a suppress with threshold action"""

class EventruleactionscommonResponse(APIResponse):
    """Response model for Eventruleactionscommon"""
    data: Optional[Eventruleactionscommon] = None

class EventruleactionscommonListResponse(APIResponse):
    """List response model for Eventruleactionscommon"""
    data: List[Eventruleactionscommon] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
