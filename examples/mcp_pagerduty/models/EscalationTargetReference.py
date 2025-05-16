"""Model for EscalationTargetReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Escalationtargetreference(BaseModel):
    """Escalationtargetreference model"""


class EscalationtargetreferenceResponse(APIResponse):
    """Response model for Escalationtargetreference"""
    data: Optional[Escalationtargetreference] = None

class EscalationtargetreferenceListResponse(APIResponse):
    """List response model for Escalationtargetreference"""
    data: List[Escalationtargetreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
