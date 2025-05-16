"""Model for AcknowledgerReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Acknowledgerreference(BaseModel):
    """Acknowledgerreference model"""


class AcknowledgerreferenceResponse(APIResponse):
    """Response model for Acknowledgerreference"""
    data: Optional[Acknowledgerreference] = None

class AcknowledgerreferenceListResponse(APIResponse):
    """List response model for Acknowledgerreference"""
    data: List[Acknowledgerreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
