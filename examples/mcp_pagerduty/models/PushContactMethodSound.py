"""Model for PushContactMethodSound"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Pushcontactmethodsound(BaseModel):
    """Pushcontactmethodsound model"""

    type: Optional[str] = None
    """The type of sound."""
    file: Optional[str] = None
    """The sound file name."""

class PushcontactmethodsoundResponse(APIResponse):
    """Response model for Pushcontactmethodsound"""
    data: Optional[Pushcontactmethodsound] = None

class PushcontactmethodsoundListResponse(APIResponse):
    """List response model for Pushcontactmethodsound"""
    data: List[Pushcontactmethodsound] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
