"""Model for AutomationActionsProcessAutomationJobActionPutBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsprocessautomationjobactionputbody(BaseModel):
    """Automationactionsprocessautomationjobactionputbody model"""


class AutomationactionsprocessautomationjobactionputbodyResponse(APIResponse):
    """Response model for Automationactionsprocessautomationjobactionputbody"""
    data: Optional[Automationactionsprocessautomationjobactionputbody] = None

class AutomationactionsprocessautomationjobactionputbodyListResponse(APIResponse):
    """List response model for Automationactionsprocessautomationjobactionputbody"""
    data: List[Automationactionsprocessautomationjobactionputbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
