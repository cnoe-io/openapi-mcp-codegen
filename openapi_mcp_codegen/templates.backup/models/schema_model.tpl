{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""Model for {{ model_name }}"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class {{ model_name }}(BaseModel):
    """{{ description or model_name + ' model' }}"""
{% for prop in properties %}
    {{ prop.name }}: {{ prop.type }}{% if not prop.required %} = None{% endif %}
    {% if prop.description %}"""{{ prop.description }}"""{% endif %}
{% endfor %}


class {{ model_name }}Response(APIResponse):
    """Response model for {{ model_name }}"""
    data: Optional[{{ model_name }}] = None


class {{ model_name }}ListResponse(APIResponse):
    """List response model for {{ model_name }}"""
    data: List[{{ model_name }}] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
