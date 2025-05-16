"""Model for AddonReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Addonreference(BaseModel):
    """Addonreference model"""


class AddonreferenceResponse(APIResponse):
    """Response model for Addonreference"""
    data: Optional[Addonreference] = None

class AddonreferenceListResponse(APIResponse):
    """List response model for Addonreference"""
    data: List[Addonreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
