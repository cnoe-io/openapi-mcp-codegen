"""Model for PushContactMethod"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Pushcontactmethod(BaseModel):
    """The Push Contact Method of the User."""


class PushcontactmethodResponse(APIResponse):
    """Response model for Pushcontactmethod"""
    data: Optional[Pushcontactmethod] = None

class PushcontactmethodListResponse(APIResponse):
    """List response model for Pushcontactmethod"""
    data: List[Pushcontactmethod] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
