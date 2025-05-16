"""Model for NotificationRule"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Notificationrule(BaseModel):
    """Notificationrule model"""


class NotificationruleResponse(APIResponse):
    """Response model for Notificationrule"""
    data: Optional[Notificationrule] = None

class NotificationruleListResponse(APIResponse):
    """List response model for Notificationrule"""
    data: List[Notificationrule] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
