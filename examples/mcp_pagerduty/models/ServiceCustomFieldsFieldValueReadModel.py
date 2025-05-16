"""Model for ServiceCustomFieldsFieldValueReadModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldvaluereadmodel(BaseModel):
    """Servicecustomfieldsfieldvaluereadmodel model"""

    data_type: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    field_type: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    """Determines the type of the reference."""
    value: Optional[str] = None

class ServicecustomfieldsfieldvaluereadmodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldvaluereadmodel"""
    data: Optional[Servicecustomfieldsfieldvaluereadmodel] = None

class ServicecustomfieldsfieldvaluereadmodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldvaluereadmodel"""
    data: List[Servicecustomfieldsfieldvaluereadmodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
