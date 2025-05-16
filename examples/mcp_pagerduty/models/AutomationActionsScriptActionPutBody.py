"""Model for AutomationActionsScriptActionPutBody"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsscriptactionputbody(BaseModel):
    """Automationactionsscriptactionputbody model"""


class AutomationactionsscriptactionputbodyResponse(APIResponse):
    """Response model for Automationactionsscriptactionputbody"""
    data: Optional[Automationactionsscriptactionputbody] = None

class AutomationactionsscriptactionputbodyListResponse(APIResponse):
    """List response model for Automationactionsscriptactionputbody"""
    data: List[Automationactionsscriptactionputbody] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
