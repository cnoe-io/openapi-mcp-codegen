"""Model for Order"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Order(BaseModel):
    """Order model"""

    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    shipDate: Optional[str] = None
    status: Optional[str] = None
    """Order Status"""
    complete: Optional[bool] = None

class OrderResponse(APIResponse):
    """Response model for Order"""
    data: Optional[Order] = None

class OrderListResponse(APIResponse):
    """List response model for Order"""
    data: List[Order] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
