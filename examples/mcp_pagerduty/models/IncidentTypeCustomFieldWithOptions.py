"""Model for IncidentTypeCustomFieldWithOptions"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenttypecustomfieldwithoptions(BaseModel):
    """Incidenttypecustomfieldwithoptions model"""

    enabled: bool
    """Whether the custom field is enabled."""
    id: str
    """The ID of the resource."""
    name: str
    type: str
    self: str
    """The API show URL at which the object is accessible"""
    description: Optional[str] = None
    field_type: str
    data_type: str
    updated_at: str
    """The date/time the object was last updated."""
    created_at: str
    """The date/time the object was created at."""
    display_name: str
    default_value: Optional[str] = None
    incident_type: str
    """The id of the incident type the custom field is associated with."""
    summary: str
    """A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to `name`, though it is not intended to be an identifier."""
    field_options: Optional[List[Dict]] = None
    """The options for the custom field. Applies only to `single_value_fixed` and `multi_value_fixed` field types. Optionally included in response based on query parameter."""

class IncidenttypecustomfieldwithoptionsResponse(APIResponse):
    """Response model for Incidenttypecustomfieldwithoptions"""
    data: Optional[Incidenttypecustomfieldwithoptions] = None

class IncidenttypecustomfieldwithoptionsListResponse(APIResponse):
    """List response model for Incidenttypecustomfieldwithoptions"""
    data: List[Incidenttypecustomfieldwithoptions] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
