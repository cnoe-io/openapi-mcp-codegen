"""Model for RelatedIncidentMachineLearningRelationship"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Relatedincidentmachinelearningrelationship(BaseModel):
    """The data for a type of relationship where the Incident is related due to our machine learning algorithm.
"""

    grouping_classification: Optional[str] = None
    """The classification for why this Related Incident was grouped into this group.
Values can be one of: [similar_contents, prior_feedback], where:
similar_contents - The Related Incident was due to similar contents of the Incidents.
prior_feedback - The Related Incident was determined to be related, based on User feedback or Incident merge/unmerge actions.
"""
    user_feedback: Optional[Dict] = None
    """The feedback provided from Users to influence the machine learning algorithm for future Related Incidents."""

class RelatedincidentmachinelearningrelationshipResponse(APIResponse):
    """Response model for Relatedincidentmachinelearningrelationship"""
    data: Optional[Relatedincidentmachinelearningrelationship] = None

class RelatedincidentmachinelearningrelationshipListResponse(APIResponse):
    """List response model for Relatedincidentmachinelearningrelationship"""
    data: List[Relatedincidentmachinelearningrelationship] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
