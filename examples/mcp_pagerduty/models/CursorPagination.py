"""Model for CursorPagination"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Cursorpagination(BaseModel):
    """Cursorpagination model"""

    limit: int
    """The minimum of the `limit` parameter used in the request or the maximum request size of the API."""
    next_cursor: str
    """An opaque string than will deliver the next set of results when provided as the `cursor` parameter in a subsequent request.  A `null` value for this field indicates that there are no additional results.
"""

class CursorpaginationResponse(APIResponse):
    """Response model for Cursorpagination"""
    data: Optional[Cursorpagination] = None

class CursorpaginationListResponse(APIResponse):
    """List response model for Cursorpagination"""
    data: List[Cursorpagination] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
