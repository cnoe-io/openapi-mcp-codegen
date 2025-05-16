"""Model for VendorReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Vendorreference(BaseModel):
    """Vendorreference model"""


class VendorreferenceResponse(APIResponse):
    """Response model for Vendorreference"""
    data: Optional[Vendorreference] = None

class VendorreferenceListResponse(APIResponse):
    """List response model for Vendorreference"""
    data: List[Vendorreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
