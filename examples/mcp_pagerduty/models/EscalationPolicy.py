"""Model for EscalationPolicy"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Escalationpolicy(BaseModel):
    """Escalationpolicy model"""


class EscalationpolicyResponse(APIResponse):
    """Response model for Escalationpolicy"""
    data: Optional[Escalationpolicy] = None

class EscalationpolicyListResponse(APIResponse):
    """List response model for Escalationpolicy"""
    data: List[Escalationpolicy] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
