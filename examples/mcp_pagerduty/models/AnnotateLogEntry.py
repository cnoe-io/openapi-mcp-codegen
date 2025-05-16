"""Model for AnnotateLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Annotatelogentry(BaseModel):
    """Annotatelogentry model"""


class AnnotatelogentryResponse(APIResponse):
    """Response model for Annotatelogentry"""
    data: Optional[Annotatelogentry] = None

class AnnotatelogentryListResponse(APIResponse):
    """List response model for Annotatelogentry"""
    data: List[Annotatelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
