"""Model for AutomationActionsProcessAutomationJobActionWithTeams"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsprocessautomationjobactionwithteams(BaseModel):
    """Automationactionsprocessautomationjobactionwithteams model"""


class AutomationactionsprocessautomationjobactionwithteamsResponse(APIResponse):
    """Response model for Automationactionsprocessautomationjobactionwithteams"""
    data: Optional[Automationactionsprocessautomationjobactionwithteams] = None

class AutomationactionsprocessautomationjobactionwithteamsListResponse(APIResponse):
    """List response model for Automationactionsprocessautomationjobactionwithteams"""
    data: List[Automationactionsprocessautomationjobactionwithteams] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
