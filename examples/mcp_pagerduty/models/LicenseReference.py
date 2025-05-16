"""Model for LicenseReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Licensereference(BaseModel):
    """Licensereference model"""


class LicensereferenceResponse(APIResponse):
    """Response model for Licensereference"""
    data: Optional[Licensereference] = None

class LicensereferenceListResponse(APIResponse):
    """List response model for Licensereference"""
    data: List[Licensereference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
