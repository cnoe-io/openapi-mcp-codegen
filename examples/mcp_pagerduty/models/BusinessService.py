"""Model for BusinessService"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Businessservice(BaseModel):
    """Businessservice model"""


class BusinessserviceResponse(APIResponse):
    """Response model for Businessservice"""
    data: Optional[Businessservice] = None

class BusinessserviceListResponse(APIResponse):
    """List response model for Businessservice"""
    data: List[Businessservice] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
