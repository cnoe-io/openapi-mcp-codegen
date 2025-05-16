"""Model for Context"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Context(BaseModel):
    """Context model"""

    type: str
    """The type of context being attached to the incident."""
    href: Optional[str] = None
    """The link's target url"""
    src: Optional[str] = None
    """The image's source url"""
    text: Optional[str] = None
    """The alternate display for an image"""

class ContextResponse(APIResponse):
    """Response model for Context"""
    data: Optional[Context] = None

class ContextListResponse(APIResponse):
    """List response model for Context"""
    data: List[Context] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
