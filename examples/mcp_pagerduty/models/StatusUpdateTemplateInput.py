"""Model for StatusUpdateTemplateInput"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Statusupdatetemplateinput(BaseModel):
    """Statusupdatetemplateinput model"""

    incident_id: Optional[str] = None
    """The incident id to render the template for"""
    status_update: Optional[Dict] = None
    external: Optional[str] = None
    """An optional object collection that can be referenced in the template."""

class StatusupdatetemplateinputResponse(APIResponse):
    """Response model for Statusupdatetemplateinput"""
    data: Optional[Statusupdatetemplateinput] = None

class StatusupdatetemplateinputListResponse(APIResponse):
    """List response model for Statusupdatetemplateinput"""
    data: List[Statusupdatetemplateinput] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
