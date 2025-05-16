"""Model for TagReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Tagreference(BaseModel):
    """Tagreference model"""


class TagreferenceResponse(APIResponse):
    """Response model for Tagreference"""
    data: Optional[Tagreference] = None

class TagreferenceListResponse(APIResponse):
    """List response model for Tagreference"""
    data: List[Tagreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
