"""Model for EditableTemplate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Editabletemplate(BaseModel):
    """Editabletemplate model"""

    template_type: Optional[str] = None
    """The type of template (`status_update` is the only supported template at this time)"""
    name: Optional[str] = None
    """The name of the template"""
    description: Optional[str] = None
    """Description of the template"""
    templated_fields: Optional[Dict] = None

class EditabletemplateResponse(APIResponse):
    """Response model for Editabletemplate"""
    data: Optional[Editabletemplate] = None

class EditabletemplateListResponse(APIResponse):
    """List response model for Editabletemplate"""
    data: List[Editabletemplate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
