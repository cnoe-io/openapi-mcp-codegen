"""Model for Retrieveincidentresponses"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Retrieveincidentresponses(BaseModel):
  """List of incidents returned by a query retrieval"""


class RetrieveincidentresponsesResponse(APIResponse):
  """Response model for Retrieveincidentresponses"""

  data: Optional[Retrieveincidentresponses] = None


class RetrieveincidentresponsesListResponse(APIResponse):
  """List response model for Retrieveincidentresponses"""

  data: List[Retrieveincidentresponses] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
