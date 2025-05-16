"""Model for ServiceCustomFieldsFieldCreateModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldcreatemodel(BaseModel):
    """Details of the custom field to be created."""

    data_type: str
    default_value: Optional[str] = None
    """Default values are only applied to newly created resources. Existing resources are not updated."""
    description: Optional[str] = None
    display_name: str
    enabled: Optional[str] = None
    field_options: Optional[List[str]] = None
    field_type: str
    name: str

class ServicecustomfieldsfieldcreatemodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldcreatemodel"""
    data: Optional[Servicecustomfieldsfieldcreatemodel] = None

class ServicecustomfieldsfieldcreatemodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldcreatemodel"""
    data: List[Servicecustomfieldsfieldcreatemodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
