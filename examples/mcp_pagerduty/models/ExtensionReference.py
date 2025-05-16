"""Model for ExtensionReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Extensionreference(BaseModel):
    """Extensionreference model"""


class ExtensionreferenceResponse(APIResponse):
    """Response model for Extensionreference"""
    data: Optional[Extensionreference] = None

class ExtensionreferenceListResponse(APIResponse):
    """List response model for Extensionreference"""
    data: List[Extensionreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
