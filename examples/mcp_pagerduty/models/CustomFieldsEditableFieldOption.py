"""Model for CustomFieldsEditableFieldOption"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldseditablefieldoption(BaseModel):
    """"""

    data: Optional[str] = None
    id: str
    """The ID of the resource."""
    type: str
    updated_at: str
    """The date/time the object was last updated."""
    created_at: str
    """The date/time the object was created at."""

class CustomfieldseditablefieldoptionResponse(APIResponse):
    """Response model for Customfieldseditablefieldoption"""
    data: Optional[Customfieldseditablefieldoption] = None

class CustomfieldseditablefieldoptionListResponse(APIResponse):
    """List response model for Customfieldseditablefieldoption"""
    data: List[Customfieldseditablefieldoption] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
