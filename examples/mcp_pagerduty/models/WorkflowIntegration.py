"""Model for WorkflowIntegration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Workflowintegration(BaseModel):
    """Workflowintegration model"""


class WorkflowintegrationResponse(APIResponse):
    """Response model for Workflowintegration"""
    data: Optional[Workflowintegration] = None

class WorkflowintegrationListResponse(APIResponse):
    """List response model for Workflowintegration"""
    data: List[Workflowintegration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
