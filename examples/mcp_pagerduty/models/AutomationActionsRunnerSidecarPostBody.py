"""Model for AutomationActionsRunnerSidecarPostBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnersidecarpostbody(BaseModel):
    """Automationactionsrunnersidecarpostbody model"""

    runner_type: str
    name: str
    description: str
    teams: Optional[List[str]] = None
    """The list of teams associated with the Runner"""

class AutomationactionsrunnersidecarpostbodyResponse(APIResponse):
    """Response model for Automationactionsrunnersidecarpostbody"""
    data: Optional[Automationactionsrunnersidecarpostbody] = None

class AutomationactionsrunnersidecarpostbodyListResponse(APIResponse):
    """List response model for Automationactionsrunnersidecarpostbody"""
    data: List[Automationactionsrunnersidecarpostbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
