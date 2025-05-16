"""Model for EscalationPolicyReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Escalationpolicyreference(BaseModel):
    """Escalationpolicyreference model"""


class EscalationpolicyreferenceResponse(APIResponse):
    """Response model for Escalationpolicyreference"""
    data: Optional[Escalationpolicyreference] = None

class EscalationpolicyreferenceListResponse(APIResponse):
    """List response model for Escalationpolicyreference"""
    data: List[Escalationpolicyreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
