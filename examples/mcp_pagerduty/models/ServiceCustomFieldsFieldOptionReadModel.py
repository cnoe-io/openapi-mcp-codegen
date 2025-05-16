"""Model for ServiceCustomFieldsFieldOptionReadModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Servicecustomfieldsfieldoptionreadmodel(BaseModel):
    """Servicecustomfieldsfieldoptionreadmodel model"""

    created_at: Optional[str] = None
    data: Optional[Dict] = None
    id: Optional[str] = None
    type: Optional[str] = None
    updated_at: Optional[str] = None

class ServicecustomfieldsfieldoptionreadmodelResponse(APIResponse):
    """Response model for Servicecustomfieldsfieldoptionreadmodel"""
    data: Optional[Servicecustomfieldsfieldoptionreadmodel] = None

class ServicecustomfieldsfieldoptionreadmodelListResponse(APIResponse):
    """List response model for Servicecustomfieldsfieldoptionreadmodel"""
    data: List[Servicecustomfieldsfieldoptionreadmodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
