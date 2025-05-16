"""Model for NotificationRuleReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationrulereference(BaseModel):
    """Notificationrulereference model"""


class NotificationrulereferenceResponse(APIResponse):
    """Response model for Notificationrulereference"""
    data: Optional[Notificationrulereference] = None

class NotificationrulereferenceListResponse(APIResponse):
    """List response model for Notificationrulereference"""
    data: List[Notificationrulereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
