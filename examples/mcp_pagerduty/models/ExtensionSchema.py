"""Model for ExtensionSchema"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Extensionschema(BaseModel):
    """Extensionschema model"""

    icon_url: Optional[str] = None
    """A small logo, 18-by-18 pixels."""
    logo_url: Optional[str] = None
    """A large logo, 75 pixels high and no more than 300 pixels wide."""
    label: Optional[str] = None
    """Human friendly display label"""
    key: Optional[str] = None
    """Machine friendly display label"""
    description: Optional[str] = None
    """The long description for the Extension"""
    guide_url: Optional[str] = None
    """A link to the extension's support guide"""
    send_types: Optional[List[str]] = None
    """The types of PagerDuty incident events that will activate this Extension"""
    url: Optional[str] = None
    """The url that the webhook payload will be sent to for this Extension."""

class ExtensionschemaResponse(APIResponse):
    """Response model for Extensionschema"""
    data: Optional[Extensionschema] = None

class ExtensionschemaListResponse(APIResponse):
    """List response model for Extensionschema"""
    data: List[Extensionschema] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
