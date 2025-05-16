"""Model for AutomationActionsScriptAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsscriptaction(BaseModel):
    """Automationactionsscriptaction model"""


class AutomationactionsscriptactionResponse(APIResponse):
    """Response model for Automationactionsscriptaction"""
    data: Optional[Automationactionsscriptaction] = None

class AutomationactionsscriptactionListResponse(APIResponse):
    """List response model for Automationactionsscriptaction"""
    data: List[Automationactionsscriptaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
