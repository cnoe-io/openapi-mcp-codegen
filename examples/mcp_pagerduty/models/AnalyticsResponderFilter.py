"""Model for AnalyticsResponderFilter"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsresponderfilter(BaseModel):
    """Analyticsresponderfilter model"""

    filters: Optional[Dict] = None
    """Accepts a set of filters to apply to the Incidents before aggregating.  Any incidents that do not match the included filters will be omitted from the results"""
    time_zone: Optional[str] = None
    """The time zone to use for the results and grouping."""
    order: Optional[str] = None
    """The order in which the results were sorted; asc for ascending, desc for descending."""
    order_by: Optional[str] = None
    """The column that was used for ordering the results."""

class AnalyticsresponderfilterResponse(APIResponse):
    """Response model for Analyticsresponderfilter"""
    data: Optional[Analyticsresponderfilter] = None

class AnalyticsresponderfilterListResponse(APIResponse):
    """List response model for Analyticsresponderfilter"""
    data: List[Analyticsresponderfilter] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
