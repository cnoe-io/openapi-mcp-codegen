"""Model for IncidentWorkflowAction"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflowaction(BaseModel):
    """Incidentworkflowaction model"""


class IncidentworkflowactionResponse(APIResponse):
    """Response model for Incidentworkflowaction"""
    data: Optional[Incidentworkflowaction] = None

class IncidentworkflowactionListResponse(APIResponse):
    """List response model for Incidentworkflowaction"""
    data: List[Incidentworkflowaction] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
