"""Model for MatchPredicate"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Matchpredicate(BaseModel):
    """Matchpredicate model"""

    type: str
    matcher: Optional[str] = None
    """Required if the type is `contains`, `exactly` or `regex`."""
    part: str
    """The email field that will attempt to use the matcher expression. Required if the type is `contains`, `exactly` or `regex`."""
    children: List[str]
    """Additional matchers to be run. Must be not empty if the type is `all`, `any`, or `not`."""

class MatchpredicateResponse(APIResponse):
    """Response model for Matchpredicate"""
    data: Optional[Matchpredicate] = None

class MatchpredicateListResponse(APIResponse):
    """List response model for Matchpredicate"""
    data: List[Matchpredicate] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
