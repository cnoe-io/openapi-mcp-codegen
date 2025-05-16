"""Model for EmailParser"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Emailparser(BaseModel):
    """Emailparser model"""

    action: str
    match_predicate: str
    value_extractors: Optional[List[Dict]] = None
    """Additional values that will be pulled in to the Incident object. Exactly one value extractor must have a `value_name` of `incident_key`."""

class EmailparserResponse(APIResponse):
    """Response model for Emailparser"""
    data: Optional[Emailparser] = None

class EmailparserListResponse(APIResponse):
    """List response model for Emailparser"""
    data: List[Emailparser] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
