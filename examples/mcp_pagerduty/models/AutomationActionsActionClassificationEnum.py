"""Model for AutomationActionsActionClassificationEnum"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsactionclassificationenum(BaseModel):
    """Automationactionsactionclassificationenum model"""


class AutomationactionsactionclassificationenumResponse(APIResponse):
    """Response model for Automationactionsactionclassificationenum"""
    data: Optional[Automationactionsactionclassificationenum] = None

class AutomationactionsactionclassificationenumListResponse(APIResponse):
    """List response model for Automationactionsactionclassificationenum"""
    data: List[Automationactionsactionclassificationenum] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
