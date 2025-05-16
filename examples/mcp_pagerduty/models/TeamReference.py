"""Model for TeamReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Teamreference(BaseModel):
    """Teamreference model"""


class TeamreferenceResponse(APIResponse):
    """Response model for Teamreference"""
    data: Optional[Teamreference] = None

class TeamreferenceListResponse(APIResponse):
    """List response model for Teamreference"""
    data: List[Teamreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
