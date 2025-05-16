"""Model for AutomationActionsProcessAutomationJobAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsprocessautomationjobaction(BaseModel):
    """Automationactionsprocessautomationjobaction model"""


class AutomationactionsprocessautomationjobactionResponse(APIResponse):
    """Response model for Automationactionsprocessautomationjobaction"""
    data: Optional[Automationactionsprocessautomationjobaction] = None

class AutomationactionsprocessautomationjobactionListResponse(APIResponse):
    """List response model for Automationactionsprocessautomationjobaction"""
    data: List[Automationactionsprocessautomationjobaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
