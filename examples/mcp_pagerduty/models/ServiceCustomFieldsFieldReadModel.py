"""Model for ServiceCustomFieldsFieldReadModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldreadmodel(BaseModel):
    """Details of the custom field."""

    created_at: Optional[str] = None
    """The date/time the object was created at."""
    data_type: Optional[str] = None
    default_value: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    enabled: Optional[str] = None
    field_options: Optional[List[str]] = None
    """The options for the custom field. Applies only to `single_value_fixed` and `multi_value_fixed` field types. These options are returned only if the `include[]` parameter specifies `field_options`."""
    field_type: Optional[str] = None
    id: Optional[str] = None
    """The ID of the resource."""
    name: Optional[str] = None
    self: Optional[str] = None
    """The API show URL at which the object is accessible"""
    summary: Optional[str] = None
    """A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to `display_name`."""
    type: Optional[str] = None
    updated_at: Optional[str] = None
    """The date/time the object was updated at."""

class ServicecustomfieldsfieldreadmodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldreadmodel"""
    data: Optional[Servicecustomfieldsfieldreadmodel] = None

class ServicecustomfieldsfieldreadmodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldreadmodel"""
    data: List[Servicecustomfieldsfieldreadmodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
