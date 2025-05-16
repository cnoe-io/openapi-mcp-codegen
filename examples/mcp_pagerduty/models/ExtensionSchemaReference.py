"""Model for ExtensionSchemaReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Extensionschemareference(BaseModel):
    """Extensionschemareference model"""


class ExtensionschemareferenceResponse(APIResponse):
    """Response model for Extensionschemareference"""
    data: Optional[Extensionschemareference] = None

class ExtensionschemareferenceListResponse(APIResponse):
    """List response model for Extensionschemareference"""
    data: List[Extensionschemareference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
