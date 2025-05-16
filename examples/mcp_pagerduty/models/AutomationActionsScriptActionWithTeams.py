"""Model for AutomationActionsScriptActionWithTeams"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsscriptactionwithteams(BaseModel):
    """Automationactionsscriptactionwithteams model"""


class AutomationactionsscriptactionwithteamsResponse(APIResponse):
    """Response model for Automationactionsscriptactionwithteams"""
    data: Optional[Automationactionsscriptactionwithteams] = None

class AutomationactionsscriptactionwithteamsListResponse(APIResponse):
    """List response model for Automationactionsscriptactionwithteams"""
    data: List[Automationactionsscriptactionwithteams] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
