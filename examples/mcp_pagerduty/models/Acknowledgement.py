"""Model for Acknowledgement"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Acknowledgement(BaseModel):
    """Acknowledgement model"""

    at: str
    """Time at which the acknowledgement was created."""
    acknowledger: str

class AcknowledgementResponse(APIResponse):
    """Response model for Acknowledgement"""
    data: Optional[Acknowledgement] = None

class AcknowledgementListResponse(APIResponse):
    """List response model for Acknowledgement"""
    data: List[Acknowledgement] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
