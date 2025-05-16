"""Model for AutomationActionsRunnerStatusEnum"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnerstatusenum(BaseModel):
    """Configured -- Runner has connected to the backend at least once 
NotConfigured -- Runner has never connected to backend
"""


class AutomationactionsrunnerstatusenumResponse(APIResponse):
    """Response model for Automationactionsrunnerstatusenum"""
    data: Optional[Automationactionsrunnerstatusenum] = None

class AutomationactionsrunnerstatusenumListResponse(APIResponse):
    """List response model for Automationactionsrunnerstatusenum"""
    data: List[Automationactionsrunnerstatusenum] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
