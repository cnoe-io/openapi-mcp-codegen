"""Model for CustomFieldsField"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldsfield(BaseModel):
    """Customfieldsfield model"""


class CustomfieldsfieldResponse(APIResponse):
    """Response model for Customfieldsfield"""
    data: Optional[Customfieldsfield] = None

class CustomfieldsfieldListResponse(APIResponse):
    """List response model for Customfieldsfield"""
    data: List[Customfieldsfield] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
