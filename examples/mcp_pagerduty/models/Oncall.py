"""Model for Oncall"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Oncall(BaseModel):
    """Oncall model"""

    escalation_policy: Optional[str] = None
    user: Optional[str] = None
    schedule: Optional[str] = None
    escalation_level: Optional[int] = None
    """The escalation level for the on-call."""
    start: Optional[str] = None
    """The start of the on-call. If `null`, the on-call is a permanent user on-call."""
    end: Optional[str] = None
    """The end of the on-call. If `null`, the user does not go off-call."""

class OncallResponse(APIResponse):
    """Response model for Oncall"""
    data: Optional[Oncall] = None

class OncallListResponse(APIResponse):
    """List response model for Oncall"""
    data: List[Oncall] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
