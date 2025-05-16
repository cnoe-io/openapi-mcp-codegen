"""Model for OrchestrationRouter"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationrouter(BaseModel):
    """Orchestrationrouter model"""


class OrchestrationrouterResponse(APIResponse):
    """Response model for Orchestrationrouter"""
    data: Optional[Orchestrationrouter] = None

class OrchestrationrouterListResponse(APIResponse):
    """List response model for Orchestrationrouter"""
    data: List[Orchestrationrouter] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
