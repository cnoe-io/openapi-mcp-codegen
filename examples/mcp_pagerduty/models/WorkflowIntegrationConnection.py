"""Model for WorkflowIntegrationConnection"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Workflowintegrationconnection(BaseModel):
    """Workflowintegrationconnection model"""


class WorkflowintegrationconnectionResponse(APIResponse):
    """Response model for Workflowintegrationconnection"""
    data: Optional[Workflowintegrationconnection] = None

class WorkflowintegrationconnectionListResponse(APIResponse):
    """List response model for Workflowintegrationconnection"""
    data: List[Workflowintegrationconnection] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
