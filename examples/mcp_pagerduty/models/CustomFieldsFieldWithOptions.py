"""Model for CustomFieldsFieldWithOptions"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldsfieldwithoptions(BaseModel):
    """Customfieldsfieldwithoptions model"""


class CustomfieldsfieldwithoptionsResponse(APIResponse):
    """Response model for Customfieldsfieldwithoptions"""
    data: Optional[Customfieldsfieldwithoptions] = None

class CustomfieldsfieldwithoptionsListResponse(APIResponse):
    """List response model for Customfieldsfieldwithoptions"""
    data: List[Customfieldsfieldwithoptions] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
