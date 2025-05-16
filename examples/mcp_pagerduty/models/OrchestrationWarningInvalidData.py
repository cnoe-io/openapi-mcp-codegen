"""Model for OrchestrationWarningInvalidData"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationwarninginvaliddata(BaseModel):
    """This rule includes invalid data for a feature item."""

    message: Optional[str] = None
    """A description of the warning and any potential side effects."""
    rule_id: Optional[str] = None
    """The ID of the rule using the feature."""
    feature: Optional[str] = None
    """The feature that includes invalid data.

Example values include:
  * `incident_custom_field_updates`
  * `escalation_policy`
  * `cache_variable:annotate`
  * `cache_variable:conditions`
  * `cache_variable:automation_actions`
"""
    feature_type: Optional[str] = None
    """Specifies the feature type of the impacted item.

Example values include:
  * `actions`
  * `conditions`
"""
    warning_type: Optional[str] = None
    """The type of warning that is being returned for the rule."""

class OrchestrationwarninginvaliddataResponse(APIResponse):
    """Response model for Orchestrationwarninginvaliddata"""
    data: Optional[Orchestrationwarninginvaliddata] = None

class OrchestrationwarninginvaliddataListResponse(APIResponse):
    """List response model for Orchestrationwarninginvaliddata"""
    data: List[Orchestrationwarninginvaliddata] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
