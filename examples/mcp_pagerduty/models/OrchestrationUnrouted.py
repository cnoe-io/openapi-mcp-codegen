"""Model for OrchestrationUnrouted"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationunrouted(BaseModel):
    """Orchestrationunrouted model"""


class OrchestrationunroutedResponse(APIResponse):
    """Response model for Orchestrationunrouted"""
    data: Optional[Orchestrationunrouted] = None

class OrchestrationunroutedListResponse(APIResponse):
    """List response model for Orchestrationunrouted"""
    data: List[Orchestrationunrouted] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
