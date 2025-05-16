"""Model for AutomationActionsAbstractAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsabstractaction(BaseModel):
    """Automationactionsabstractaction model"""


class AutomationactionsabstractactionResponse(APIResponse):
    """Response model for Automationactionsabstractaction"""
    data: Optional[Automationactionsabstractaction] = None

class AutomationactionsabstractactionListResponse(APIResponse):
    """List response model for Automationactionsabstractaction"""
    data: List[Automationactionsabstractaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
