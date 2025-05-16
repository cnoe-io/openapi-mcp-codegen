"""Model for RenderedTemplate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Renderedtemplate(BaseModel):
    """Renderedtemplate model"""

    templated_fields: Optional[Dict] = None
    warnings: Optional[Dict] = None
    """List of render warnings messages for each rendered field.
(Ex:  ["{{incident.invalid_field}} does not exist."])"""
    errors: Optional[List[str]] = None
    """List of errors"""

class RenderedtemplateResponse(APIResponse):
    """Response model for Renderedtemplate"""
    data: Optional[Renderedtemplate] = None

class RenderedtemplateListResponse(APIResponse):
    """List response model for Renderedtemplate"""
    data: List[Renderedtemplate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
