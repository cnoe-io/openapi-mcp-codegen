"""Model for Assignment"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Assignment(BaseModel):
    """Assignment model"""

    at: str
    """Time at which the assignment was created."""
    assignee: str

class AssignmentResponse(APIResponse):
    """Response model for Assignment"""
    data: Optional[Assignment] = None

class AssignmentListResponse(APIResponse):
    """List response model for Assignment"""
    data: List[Assignment] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
