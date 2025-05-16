"""Model for Reference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Reference(BaseModel):
    """Reference model"""


class ReferenceResponse(APIResponse):
    """Response model for Reference"""
    data: Optional[Reference] = None

class ReferenceListResponse(APIResponse):
    """List response model for Reference"""
    data: List[Reference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
