"""Model for EscalationRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Escalationrule(BaseModel):
    """Escalationrule model"""

    id: Optional[str] = None
    escalation_delay_in_minutes: int
    """The number of minutes before an unacknowledged incident escalates away from this rule."""
    targets: List[str]
    """The targets an incident should be assigned to upon reaching this rule."""
    escalation_rule_assignment_strategy: Optional[str] = None
    """The strategy used to assign the escalation rule to an incident."""

class EscalationruleResponse(APIResponse):
    """Response model for Escalationrule"""
    data: Optional[Escalationrule] = None

class EscalationruleListResponse(APIResponse):
    """List response model for Escalationrule"""
    data: List[Escalationrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
