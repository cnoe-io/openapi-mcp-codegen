"""Model for FieldValueChangeLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Fieldvaluechangelogentry(BaseModel):
    """Fieldvaluechangelogentry model"""


class FieldvaluechangelogentryResponse(APIResponse):
    """Response model for Fieldvaluechangelogentry"""
    data: Optional[Fieldvaluechangelogentry] = None

class FieldvaluechangelogentryListResponse(APIResponse):
    """List response model for Fieldvaluechangelogentry"""
    data: List[Fieldvaluechangelogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
