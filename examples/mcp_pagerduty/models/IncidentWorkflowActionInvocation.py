"""Model for IncidentWorkflowActionInvocation"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidentworkflowactioninvocation(BaseModel):
    """Incidentworkflowactioninvocation model"""

    id: Optional[str] = None
    type: Optional[str] = None
    action_id: Optional[str] = None
    """Reference to the Action that was invoked"""
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None

class IncidentworkflowactioninvocationResponse(APIResponse):
    """Response model for Incidentworkflowactioninvocation"""
    data: Optional[Incidentworkflowactioninvocation] = None

class IncidentworkflowactioninvocationListResponse(APIResponse):
    """List response model for Incidentworkflowactioninvocation"""
    data: List[Incidentworkflowactioninvocation] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
