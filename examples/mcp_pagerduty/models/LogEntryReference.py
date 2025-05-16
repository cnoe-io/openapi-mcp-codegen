"""Model for LogEntryReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Logentryreference(BaseModel):
    """Logentryreference model"""


class LogentryreferenceResponse(APIResponse):
    """Response model for Logentryreference"""
    data: Optional[Logentryreference] = None

class LogentryreferenceListResponse(APIResponse):
    """List response model for Logentryreference"""
    data: List[Logentryreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
