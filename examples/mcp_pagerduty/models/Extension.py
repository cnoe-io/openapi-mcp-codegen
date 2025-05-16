"""Model for Extension"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Extension(BaseModel):
    """Extension model"""


class ExtensionResponse(APIResponse):
    """Response model for Extension"""
    data: Optional[Extension] = None

class ExtensionListResponse(APIResponse):
    """List response model for Extension"""
    data: List[Extension] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
