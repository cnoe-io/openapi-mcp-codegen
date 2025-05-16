"""Model for ServiceCustomFieldsFieldValueUpdateModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldvalueupdatemodel(BaseModel):
    """During updates:
- Omitted fields remain unchanged
- Null values reset fields
- Provided values update fields

Note: All updates succeed or none are applied.
"""


class ServicecustomfieldsfieldvalueupdatemodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldvalueupdatemodel"""
    data: Optional[Servicecustomfieldsfieldvalueupdatemodel] = None

class ServicecustomfieldsfieldvalueupdatemodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldvalueupdatemodel"""
    data: List[Servicecustomfieldsfieldvalueupdatemodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
