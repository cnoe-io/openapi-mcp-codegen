"""Model for OrchestrationCacheVariableRecentValue"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationcachevariablerecentvalue(BaseModel):
    """Orchestrationcachevariablerecentvalue model"""


class OrchestrationcachevariablerecentvalueResponse(APIResponse):
    """Response model for Orchestrationcachevariablerecentvalue"""
    data: Optional[Orchestrationcachevariablerecentvalue] = None

class OrchestrationcachevariablerecentvalueListResponse(APIResponse):
    """List response model for Orchestrationcachevariablerecentvalue"""
    data: List[Orchestrationcachevariablerecentvalue] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
