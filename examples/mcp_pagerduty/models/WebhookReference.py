"""Model for WebhookReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Webhookreference(BaseModel):
    """Webhookreference model"""


class WebhookreferenceResponse(APIResponse):
    """Response model for Webhookreference"""
    data: Optional[Webhookreference] = None

class WebhookreferenceListResponse(APIResponse):
    """List response model for Webhookreference"""
    data: List[Webhookreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
