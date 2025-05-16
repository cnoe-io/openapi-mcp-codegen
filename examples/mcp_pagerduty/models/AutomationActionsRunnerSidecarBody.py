"""Model for AutomationActionsRunnerSidecarBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnersidecarbody(BaseModel):
    """Automationactionsrunnersidecarbody model"""

    name: Optional[str] = None
    description: Optional[str] = None

class AutomationactionsrunnersidecarbodyResponse(APIResponse):
    """Response model for Automationactionsrunnersidecarbody"""
    data: Optional[Automationactionsrunnersidecarbody] = None

class AutomationactionsrunnersidecarbodyListResponse(APIResponse):
    """List response model for Automationactionsrunnersidecarbody"""
    data: List[Automationactionsrunnersidecarbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
