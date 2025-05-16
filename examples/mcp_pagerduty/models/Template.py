"""Model for Template"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Template(BaseModel):
    """Template model"""


class TemplateResponse(APIResponse):
    """Response model for Template"""
    data: Optional[Template] = None

class TemplateListResponse(APIResponse):
    """List response model for Template"""
    data: List[Template] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
