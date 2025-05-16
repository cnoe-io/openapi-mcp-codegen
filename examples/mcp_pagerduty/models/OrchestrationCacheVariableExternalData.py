"""Model for OrchestrationCacheVariableExternalData"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationcachevariableexternaldata(BaseModel):
    """Orchestrationcachevariableexternaldata model"""


class OrchestrationcachevariableexternaldataResponse(APIResponse):
    """Response model for Orchestrationcachevariableexternaldata"""
    data: Optional[Orchestrationcachevariableexternaldata] = None

class OrchestrationcachevariableexternaldataListResponse(APIResponse):
    """List response model for Orchestrationcachevariableexternaldata"""
    data: List[Orchestrationcachevariableexternaldata] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
