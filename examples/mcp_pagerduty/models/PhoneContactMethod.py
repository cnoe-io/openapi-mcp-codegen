"""Model for PhoneContactMethod"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Phonecontactmethod(BaseModel):
    """The Phone Contact Method of the User, used for Voice or SMS."""


class PhonecontactmethodResponse(APIResponse):
    """Response model for Phonecontactmethod"""
    data: Optional[Phonecontactmethod] = None

class PhonecontactmethodListResponse(APIResponse):
    """List response model for Phonecontactmethod"""
    data: List[Phonecontactmethod] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
