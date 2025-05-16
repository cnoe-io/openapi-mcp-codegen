"""Model for ResolveLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Resolvelogentry(BaseModel):
    """Resolvelogentry model"""


class ResolvelogentryResponse(APIResponse):
    """Response model for Resolvelogentry"""
    data: Optional[Resolvelogentry] = None

class ResolvelogentryListResponse(APIResponse):
    """List response model for Resolvelogentry"""
    data: List[Resolvelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
