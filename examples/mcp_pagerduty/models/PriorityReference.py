"""Model for PriorityReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Priorityreference(BaseModel):
    """Priorityreference model"""


class PriorityreferenceResponse(APIResponse):
    """Response model for Priorityreference"""
    data: Optional[Priorityreference] = None

class PriorityreferenceListResponse(APIResponse):
    """List response model for Priorityreference"""
    data: List[Priorityreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
