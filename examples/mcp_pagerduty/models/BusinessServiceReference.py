"""Model for BusinessServiceReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Businessservicereference(BaseModel):
    """Businessservicereference model"""


class BusinessservicereferenceResponse(APIResponse):
    """Response model for Businessservicereference"""
    data: Optional[Businessservicereference] = None

class BusinessservicereferenceListResponse(APIResponse):
    """List response model for Businessservicereference"""
    data: List[Businessservicereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
