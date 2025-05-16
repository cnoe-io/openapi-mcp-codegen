"""Model for UserReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Userreference(BaseModel):
    """Userreference model"""


class UserreferenceResponse(APIResponse):
    """Response model for Userreference"""
    data: Optional[Userreference] = None

class UserreferenceListResponse(APIResponse):
    """List response model for Userreference"""
    data: List[Userreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
