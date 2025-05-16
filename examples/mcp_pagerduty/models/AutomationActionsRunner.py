"""Model for AutomationActionsRunner"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunner(BaseModel):
    """Automationactionsrunner model"""


class AutomationactionsrunnerResponse(APIResponse):
    """Response model for Automationactionsrunner"""
    data: Optional[Automationactionsrunner] = None

class AutomationactionsrunnerListResponse(APIResponse):
    """List response model for Automationactionsrunner"""
    data: List[Automationactionsrunner] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
