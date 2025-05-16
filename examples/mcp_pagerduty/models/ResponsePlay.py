"""Model for ResponsePlay"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Responseplay(BaseModel):
    """Responseplay model"""


class ResponseplayResponse(APIResponse):
    """Response model for Responseplay"""
    data: Optional[Responseplay] = None

class ResponseplayListResponse(APIResponse):
    """List response model for Responseplay"""
    data: List[Responseplay] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
