"""Model for AnalyticsPdAdvanceUsageFilter"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticspdadvanceusagefilter(BaseModel):
    """Analyticspdadvanceusagefilter model"""

    filters: Optional[Dict] = None
    """Accepts a set of filters to apply to the Incidents before aggregating.  Any incidents that do not match the included filters will be omitted from the results."""
    time_zone: Optional[str] = None
    """The time zone to use for the results and grouping. Must be in tzdata format. See list of accepted values [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)."""

class AnalyticspdadvanceusagefilterResponse(APIResponse):
    """Response model for Analyticspdadvanceusagefilter"""
    data: Optional[Analyticspdadvanceusagefilter] = None

class AnalyticspdadvanceusagefilterListResponse(APIResponse):
    """List response model for Analyticspdadvanceusagefilter"""
    data: List[Analyticspdadvanceusagefilter] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
