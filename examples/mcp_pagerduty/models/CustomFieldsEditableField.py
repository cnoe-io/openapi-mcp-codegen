"""Model for CustomFieldsEditableField"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldseditablefield(BaseModel):
    """Customfieldseditablefield model"""

    display_name: Optional[str] = None
    description: Optional[str] = None
    default_value: Optional[str] = None
    enabled: Optional[bool] = None
    """Whether the field is enabled."""

class CustomfieldseditablefieldResponse(APIResponse):
    """Response model for Customfieldseditablefield"""
    data: Optional[Customfieldseditablefield] = None

class CustomfieldseditablefieldListResponse(APIResponse):
    """List response model for Customfieldseditablefield"""
    data: List[Customfieldseditablefield] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
