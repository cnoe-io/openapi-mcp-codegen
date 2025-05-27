{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""Tools for {{ path }} operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from {{ mcp_server_base_package }}mcp_{{ mcp_name }}.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")

{% for func in functions %}
async def {{ func.operation_id }}({{ func.params | join(', ') }}) -> Dict[str, Any]:
    """
    {{ func.summary }}
    {{ func.description }}
    Returns:
        API response data
    """
    logger.debug("Making {{ func.method.upper() }} request to {{ path }}")
    params = {}
    data = None
    {% if 'body' in func.params | join(', ') %}
    # Add parameters to request
    if body is not None:
      data = body
    {% endif %}
    success, response = await make_api_request(
        "{{ path }}",
        method="{{ func.method.upper() }}",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

{% endfor %}
