"""Model for StatusUpdateNotificationRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statusupdatenotificationrule(BaseModel):
    """A rule for contacting the user for Incident Status Updates."""

    contact_method: str

class StatusupdatenotificationruleResponse(APIResponse):
    """Response model for Statusupdatenotificationrule"""
    data: Optional[Statusupdatenotificationrule] = None

class StatusupdatenotificationruleListResponse(APIResponse):
    """List response model for Statusupdatenotificationrule"""
    data: List[Statusupdatenotificationrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
