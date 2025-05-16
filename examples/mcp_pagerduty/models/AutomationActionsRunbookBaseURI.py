"""Model for AutomationActionsRunbookBaseURI"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsrunbookbaseuri(BaseModel):
    """The base URI of the Runbook server to connect to. May only contain alphanumeric characters, periods, underscores and dashes. Specified as the subdomain portion of an RBA host, as in <runbook_base_uri>.runbook.pagerduty.cloud"""


class AutomationactionsrunbookbaseuriResponse(APIResponse):
    """Response model for Automationactionsrunbookbaseuri"""
    data: Optional[Automationactionsrunbookbaseuri] = None

class AutomationactionsrunbookbaseuriListResponse(APIResponse):
    """List response model for Automationactionsrunbookbaseuri"""
    data: List[Automationactionsrunbookbaseuri] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
