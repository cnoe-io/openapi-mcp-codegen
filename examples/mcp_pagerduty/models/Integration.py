"""Model for Integration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Integration(BaseModel):
    """Integration model"""


class IntegrationResponse(APIResponse):
    """Response model for Integration"""
    data: Optional[Integration] = None

class IntegrationListResponse(APIResponse):
    """List response model for Integration"""
    data: List[Integration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
