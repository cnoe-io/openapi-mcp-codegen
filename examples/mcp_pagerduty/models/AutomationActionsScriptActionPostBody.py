"""Model for AutomationActionsScriptActionPostBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsscriptactionpostbody(BaseModel):
    """Automationactionsscriptactionpostbody model"""


class AutomationactionsscriptactionpostbodyResponse(APIResponse):
    """Response model for Automationactionsscriptactionpostbody"""
    data: Optional[Automationactionsscriptactionpostbody] = None

class AutomationactionsscriptactionpostbodyListResponse(APIResponse):
    """List response model for Automationactionsscriptactionpostbody"""
    data: List[Automationactionsscriptactionpostbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
