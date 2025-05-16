"""Model for CustomFieldsFieldValue"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldsfieldvalue(BaseModel):
    """Customfieldsfieldvalue model"""

    id: str
    """Id of the field."""
    name: str
    """The name of the field. May include ASCII characters, specifically lowercase letters, digits, and underescores. The `name` for a Field must be unique and cannot be changed once created."""
    type: str
    """Determines the type of the reference."""
    display_name: str
    """The human-readable name of the field. This must be unique across an account."""
    field_type: str
    """The type of data this field contains. In combination with the `data_type` field."""
    data_type: str
    """The kind of data the custom field is allowed to contain."""
    description: str
    """A description of the data this field contains."""
    value: str

class CustomfieldsfieldvalueResponse(APIResponse):
    """Response model for Customfieldsfieldvalue"""
    data: Optional[Customfieldsfieldvalue] = None

class CustomfieldsfieldvalueListResponse(APIResponse):
    """List response model for Customfieldsfieldvalue"""
    data: List[Customfieldsfieldvalue] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
