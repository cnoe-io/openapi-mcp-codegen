"""Model for ContactMethodReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Contactmethodreference(BaseModel):
    """Contactmethodreference model"""


class ContactmethodreferenceResponse(APIResponse):
    """Response model for Contactmethodreference"""
    data: Optional[Contactmethodreference] = None

class ContactmethodreferenceListResponse(APIResponse):
    """List response model for Contactmethodreference"""
    data: List[Contactmethodreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
