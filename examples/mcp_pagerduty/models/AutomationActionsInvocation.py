"""Model for AutomationActionsInvocation"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsinvocation(BaseModel):
    """Automationactionsinvocation model"""


class AutomationactionsinvocationResponse(APIResponse):
    """Response model for Automationactionsinvocation"""
    data: Optional[Automationactionsinvocation] = None

class AutomationactionsinvocationListResponse(APIResponse):
    """List response model for Automationactionsinvocation"""
    data: List[Automationactionsinvocation] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
