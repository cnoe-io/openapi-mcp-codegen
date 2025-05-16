"""Model for CustomFieldsEditableFieldValue"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldseditablefieldvalue(BaseModel):
    """Customfieldseditablefieldvalue model"""


class CustomfieldseditablefieldvalueResponse(APIResponse):
    """Response model for Customfieldseditablefieldvalue"""
    data: Optional[Customfieldseditablefieldvalue] = None

class CustomfieldseditablefieldvalueListResponse(APIResponse):
    """List response model for Customfieldseditablefieldvalue"""
    data: List[Customfieldseditablefieldvalue] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
