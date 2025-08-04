"""Model for Sendalertsoncemutingperiodhasended"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Sendalertsoncemutingperiodhasended(BaseModel):
  """Controls notifications after the muting period ends"""


class SendalertsoncemutingperiodhasendedResponse(APIResponse):
  """Response model for Sendalertsoncemutingperiodhasended"""

  data: Optional[Sendalertsoncemutingperiodhasended] = None


class SendalertsoncemutingperiodhasendedListResponse(APIResponse):
  """List response model for Sendalertsoncemutingperiodhasended"""

  data: List[Sendalertsoncemutingperiodhasended] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
