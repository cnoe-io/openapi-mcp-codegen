"""Model for AutomationActionsUserPermissions"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsuserpermissions(BaseModel):
    """Automationactionsuserpermissions model"""

    permissions: List[str]

class AutomationactionsuserpermissionsResponse(APIResponse):
    """Response model for Automationactionsuserpermissions"""
    data: Optional[Automationactionsuserpermissions] = None

class AutomationactionsuserpermissionsListResponse(APIResponse):
    """List response model for Automationactionsuserpermissions"""
    data: List[Automationactionsuserpermissions] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
