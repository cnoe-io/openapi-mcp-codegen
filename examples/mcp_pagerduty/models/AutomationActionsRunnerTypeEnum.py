"""Model for AutomationActionsRunnerTypeEnum"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunnertypeenum(BaseModel):
    """sidecar -- The runner is backed by an external sidecar that polls for invocations.
runbook -- The runner communicates directly with a runbook instance.
"""


class AutomationactionsrunnertypeenumResponse(APIResponse):
    """Response model for Automationactionsrunnertypeenum"""
    data: Optional[Automationactionsrunnertypeenum] = None

class AutomationactionsrunnertypeenumListResponse(APIResponse):
    """List response model for Automationactionsrunnertypeenum"""
    data: List[Automationactionsrunnertypeenum] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
