"""Model for AutomationActionsRunnerRunbookPostBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnerrunbookpostbody(BaseModel):
    """Automationactionsrunnerrunbookpostbody model"""

    runner_type: str
    name: str
    description: str
    runbook_base_uri: str
    runbook_api_key: str
    """The API key to connect to the Runbook server with. If omitted, the previously stored value will remain unchanged"""
    teams: Optional[List[str]] = None
    """The list of teams associated with the Runner"""

class AutomationactionsrunnerrunbookpostbodyResponse(APIResponse):
    """Response model for Automationactionsrunnerrunbookpostbody"""
    data: Optional[Automationactionsrunnerrunbookpostbody] = None

class AutomationactionsrunnerrunbookpostbodyListResponse(APIResponse):
    """List response model for Automationactionsrunnerrunbookpostbody"""
    data: List[Automationactionsrunnerrunbookpostbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
