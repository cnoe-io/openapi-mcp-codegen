"""Model for AcknowledgeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Acknowledgelogentry(BaseModel):
    """Acknowledgelogentry model"""


class AcknowledgelogentryResponse(APIResponse):
    """Response model for Acknowledgelogentry"""
    data: Optional[Acknowledgelogentry] = None

class AcknowledgelogentryListResponse(APIResponse):
    """List response model for Acknowledgelogentry"""
    data: List[Acknowledgelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
