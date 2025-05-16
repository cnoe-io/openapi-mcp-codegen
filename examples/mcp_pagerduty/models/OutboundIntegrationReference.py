"""Model for OutboundIntegrationReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Outboundintegrationreference(BaseModel):
    """Outboundintegrationreference model"""


class OutboundintegrationreferenceResponse(APIResponse):
    """Response model for Outboundintegrationreference"""
    data: Optional[Outboundintegrationreference] = None

class OutboundintegrationreferenceListResponse(APIResponse):
    """List response model for Outboundintegrationreference"""
    data: List[Outboundintegrationreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
