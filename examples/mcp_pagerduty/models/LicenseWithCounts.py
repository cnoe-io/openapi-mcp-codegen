"""Model for LicenseWithCounts"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Licensewithcounts(BaseModel):
    """Licensewithcounts model"""


class LicensewithcountsResponse(APIResponse):
    """Response model for Licensewithcounts"""
    data: Optional[Licensewithcounts] = None

class LicensewithcountsListResponse(APIResponse):
    """List response model for Licensewithcounts"""
    data: List[Licensewithcounts] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
