"""Model for AutomationActionsRunnerRunbookBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnerrunbookbody(BaseModel):
    """Automationactionsrunnerrunbookbody model"""

    name: Optional[str] = None
    description: Optional[str] = None
    runbook_base_uri: Optional[str] = None
    runbook_api_key: Optional[str] = None
    """The API key to connect to the Runbook server with. If omitted, the previously stored value will remain unchanged"""

class AutomationactionsrunnerrunbookbodyResponse(APIResponse):
    """Response model for Automationactionsrunnerrunbookbody"""
    data: Optional[Automationactionsrunnerrunbookbody] = None

class AutomationactionsrunnerrunbookbodyListResponse(APIResponse):
    """List response model for Automationactionsrunnerrunbookbody"""
    data: List[Automationactionsrunnerrunbookbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
