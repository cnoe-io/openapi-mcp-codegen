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

    OpenAPI Description:
        {{ func.description }}

    Args:
{%- for param in func.params %}
        {%- set pname = param.split(':')[0].strip() -%}
        {%- set ptype = (param.split(':')[1].strip() if ':' in param else "str") -%}
        {{ pname }} ({{ ptype }}): OpenAPI parameter corresponding to '{{ pname }}'.
{%- endfor %}

    Returns:
        Dict[str, Any]: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    logger.debug("Making {{ func.method.upper() }} request to {{ path }}")
    params = {}
    {% for param in func.params if param != "body" %}
    if {{ param.split(':')[0].strip() }} is not None:
      params["{{ param.split(':')[0].strip() }}"] = {{ param.split(':')[0].strip() }}
    {% endfor %}
    data = None
    {# Build outbound query parameters from param_ prefixed parameters #}
{% for param in func.params %}
    {%- set param_name = param.split(':')[0] | trim %}
    {% if param_name.startswith("param_") %}
    params["{{ param_name[6:] }}"] = {{ param_name }}
    {% endif %}
{% endfor %}

    {# Build outbound request body data from body_ prefixed parameters #}
    data = {}
{% for param in func.params %}
    {%- set param_name = param.split(':')[0] | trim %}
    {% if param_name.startswith("body_") %}
    data["{{ param_name[5:] }}"] = {{ param_name }}
    {% endif %}
{% endfor %}
    if not data:
        data = None
    success, response = await make_api_request(
        f"{{ func.formatted_path }}",
        method="{{ func.method.upper() }}",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

{% endfor %}
