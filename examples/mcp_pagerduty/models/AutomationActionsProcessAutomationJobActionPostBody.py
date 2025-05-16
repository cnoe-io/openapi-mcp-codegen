"""Model for AutomationActionsProcessAutomationJobActionPostBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsprocessautomationjobactionpostbody(BaseModel):
    """Automationactionsprocessautomationjobactionpostbody model"""


class AutomationactionsprocessautomationjobactionpostbodyResponse(APIResponse):
    """Response model for Automationactionsprocessautomationjobactionpostbody"""
    data: Optional[Automationactionsprocessautomationjobactionpostbody] = None

class AutomationactionsprocessautomationjobactionpostbodyListResponse(APIResponse):
    """List response model for Automationactionsprocessautomationjobactionpostbody"""
    data: List[Automationactionsprocessautomationjobactionpostbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
