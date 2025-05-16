"""Model for EntityReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Entityreference(BaseModel):
    """Entityreference model"""


class EntityreferenceResponse(APIResponse):
    """Response model for Entityreference"""
    data: Optional[Entityreference] = None

class EntityreferenceListResponse(APIResponse):
    """List response model for Entityreference"""
    data: List[Entityreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
