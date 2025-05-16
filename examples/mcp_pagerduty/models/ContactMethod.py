"""Model for ContactMethod"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Contactmethod(BaseModel):
    """Contactmethod model"""


class ContactmethodResponse(APIResponse):
    """Response model for Contactmethod"""
    data: Optional[Contactmethod] = None

class ContactmethodListResponse(APIResponse):
    """List response model for Contactmethod"""
    data: List[Contactmethod] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
