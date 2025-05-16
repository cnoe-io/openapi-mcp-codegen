"""Model for CustomFieldValueChangeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Customfieldvaluechangelogentry(BaseModel):
    """Customfieldvaluechangelogentry model"""


class CustomfieldvaluechangelogentryResponse(APIResponse):
    """Response model for Customfieldvaluechangelogentry"""
    data: Optional[Customfieldvaluechangelogentry] = None

class CustomfieldvaluechangelogentryListResponse(APIResponse):
    """List response model for Customfieldvaluechangelogentry"""
    data: List[Customfieldvaluechangelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
