"""Model for EmailContactMethod"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Emailcontactmethod(BaseModel):
    """The Email Contact Method of the User."""


class EmailcontactmethodResponse(APIResponse):
    """Response model for Emailcontactmethod"""
    data: Optional[Emailcontactmethod] = None

class EmailcontactmethodListResponse(APIResponse):
    """List response model for Emailcontactmethod"""
    data: List[Emailcontactmethod] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
