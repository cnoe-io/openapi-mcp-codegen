"""Model for Vendor"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Vendor(BaseModel):
    """Vendor model"""


class VendorResponse(APIResponse):
    """Response model for Vendor"""
    data: Optional[Vendor] = None

class VendorListResponse(APIResponse):
    """List response model for Vendor"""
    data: List[Vendor] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
