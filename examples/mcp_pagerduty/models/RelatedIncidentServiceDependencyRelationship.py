"""Model for RelatedIncidentServiceDependencyRelationship"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Relatedincidentservicedependencyrelationship(BaseModel):
    """The data for a type of relationship where the Incident is related due to Business or Technical Service dependencies.

Both `dependent_services` and `supporting_services` are returned to signify the dependencies between the Services
that the Incident and Related Incident belong to.

Each Service reference returned in the list of supporting and dependent Services has a type of:
[business_service_reference, technical_service_reference].
"""

    dependent_services: Optional[List[str]] = None
    supporting_services: Optional[List[str]] = None

class RelatedincidentservicedependencyrelationshipResponse(APIResponse):
    """Response model for Relatedincidentservicedependencyrelationship"""
    data: Optional[Relatedincidentservicedependencyrelationship] = None

class RelatedincidentservicedependencyrelationshipListResponse(APIResponse):
    """List response model for Relatedincidentservicedependencyrelationship"""
    data: List[Relatedincidentservicedependencyrelationship] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
