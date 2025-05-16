"""Model for ServiceOrchestration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Serviceorchestration(BaseModel):
    """Serviceorchestration model"""


class ServiceorchestrationResponse(APIResponse):
    """Response model for Serviceorchestration"""
    data: Optional[Serviceorchestration] = None

class ServiceorchestrationListResponse(APIResponse):
    """List response model for Serviceorchestration"""
    data: List[Serviceorchestration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
