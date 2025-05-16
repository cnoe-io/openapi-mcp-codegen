"""Model for IncidentTypeCustomFields"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Incidenttypecustomfields(BaseModel):
    """Incidenttypecustomfields model"""

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
    """The date/time the custom field was last updated."""
    created_at: str
    """The date/time the custom field was created at."""
    display_name: str
    default_value: Optional[str] = None
    incident_type: str
    """The id of the incident type the custom field is associated with."""
    summary: str
    """A short-form, server-generated string that provides succinct, important information about an object suitable for primary labeling of an entity in a client. In many cases, this will be identical to `name`, though it is not intended to be an identifier."""
    field_options: List[str]
    """The options for the custom field."""

class IncidenttypecustomfieldsResponse(APIResponse):
    """Response model for Incidenttypecustomfields"""
    data: Optional[Incidenttypecustomfields] = None

class IncidenttypecustomfieldsListResponse(APIResponse):
    """List response model for Incidenttypecustomfields"""
    data: List[Incidenttypecustomfields] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
