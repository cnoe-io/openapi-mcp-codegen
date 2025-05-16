"""Model for ServiceCustomFieldsFieldOptionUpdateModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldoptionupdatemodel(BaseModel):
    """An option for a custom field. Can only be applied to fields with a `field_type` of `single_value_fixed` or `multi_value_fixed`."""

    data: Dict
    """The data content of the field option."""

class ServicecustomfieldsfieldoptionupdatemodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldoptionupdatemodel"""
    data: Optional[Servicecustomfieldsfieldoptionupdatemodel] = None

class ServicecustomfieldsfieldoptionupdatemodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldoptionupdatemodel"""
    data: List[Servicecustomfieldsfieldoptionupdatemodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
