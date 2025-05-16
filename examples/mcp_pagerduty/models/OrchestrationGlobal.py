"""Model for OrchestrationGlobal"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationglobal(BaseModel):
    """Orchestrationglobal model"""


class OrchestrationglobalResponse(APIResponse):
    """Response model for Orchestrationglobal"""
    data: Optional[Orchestrationglobal] = None

class OrchestrationglobalListResponse(APIResponse):
    """List response model for Orchestrationglobal"""
    data: List[Orchestrationglobal] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
