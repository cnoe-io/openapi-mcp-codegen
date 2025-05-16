"""Model for CustomFieldsFieldOption"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldsfieldoption(BaseModel):
    """Customfieldsfieldoption model"""


class CustomfieldsfieldoptionResponse(APIResponse):
    """Response model for Customfieldsfieldoption"""
    data: Optional[Customfieldsfieldoption] = None

class CustomfieldsfieldoptionListResponse(APIResponse):
    """List response model for Customfieldsfieldoption"""
    data: List[Customfieldsfieldoption] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
