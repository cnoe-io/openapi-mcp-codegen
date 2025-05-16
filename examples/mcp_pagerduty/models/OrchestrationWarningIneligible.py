"""Model for OrchestrationWarningIneligible"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationwarningineligible(BaseModel):
    """This rule is using a feature that is currently unavailable on the current account plan."""

    message: Optional[str] = None
    """A description of the warning and any potential side effects."""
    rule_id: Optional[str] = None
    """The ID of the rule using the feature."""
    feature: Optional[str] = None
    """The feature that the current account plan does not have access to.

Example values include:
* `threshold_condition`
* `nested_rules`
* `suspend`
* `automation_actions`
* `cache_variable:automation_actions`
* `cache_variable:annotate`
* `variables`
* `interpolation:annotate`
* `interpolation:extractions`
* `interpolation:incident_custom_field_updates`
* `suppress`
* `incident_custom_field_updates`
* `dynamic_route_to`
* `escalation_policy`
"""
    feature_type: Optional[str] = None
    """Specifies whether the feature is a part of the rule's conditions, or its actions.

Example values include:
* `conditions`
* `actions`
* `nested_rules`
* `global_orchestrations`
"""
    warning_type: Optional[str] = None
    """The type of warning that is being returned for the rule."""

class OrchestrationwarningineligibleResponse(APIResponse):
    """Response model for Orchestrationwarningineligible"""
    data: Optional[Orchestrationwarningineligible] = None

class OrchestrationwarningineligibleListResponse(APIResponse):
    """List response model for Orchestrationwarningineligible"""
    data: List[Orchestrationwarningineligible] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
