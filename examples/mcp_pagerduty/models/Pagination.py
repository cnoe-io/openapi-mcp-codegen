"""Model for Pagination"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Pagination(BaseModel):
    """Pagination model"""

    offset: Optional[int] = None
    """Echoes offset pagination property."""
    limit: Optional[int] = None
    """Echoes limit pagination property."""
    more: Optional[bool] = None
    """Indicates if there are additional records to return"""
    total: Optional[int] = None
    """The total number of records matching the given query."""

class PaginationResponse(APIResponse):
    """Response model for Pagination"""
    data: Optional[Pagination] = None

class PaginationListResponse(APIResponse):
    """List response model for Pagination"""
    data: List[Pagination] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
