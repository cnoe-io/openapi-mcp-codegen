"""Model for ServiceCustomFieldsFieldUpdateModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldupdatemodel(BaseModel):
    """Details of the custom field to be updated."""

    default_value: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    enabled: Optional[str] = None
    field_options: Optional[List[str]] = None
    """List of field options to update, insert or delete. This field supports several behaviors:
  - Empty array: Deletes all field options
  - Omitting the `field_options` array entirely: Preserves all existing options
  - Not listing an existing option: Deletes that option (unless it's the current default value)
"""

class ServicecustomfieldsfieldupdatemodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldupdatemodel"""
    data: Optional[Servicecustomfieldsfieldupdatemodel] = None

class ServicecustomfieldsfieldupdatemodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldupdatemodel"""
    data: List[Servicecustomfieldsfieldupdatemodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
