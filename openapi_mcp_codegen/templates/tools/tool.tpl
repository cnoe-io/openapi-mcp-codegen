{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""Tools for {{ path }} operations"""

import logging
from typing import Dict, Any, Optional, List, Literal
from pydantic import BaseModel
from {{ mcp_server_base_package }}mcp_{{ mcp_name }}.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")

{% for func in functions %}
async def {{ func.operation_id }}({{ func.params | join(', ') }}) -> Any:
    """
    {{ func.summary }}

    OpenAPI Description:
        {{ func.description }}

    Args:
    {{ newline }}
    {%- for param in func.params_info %}
        {{ param.name }} ({{ param.type }}):{% if param.description %} {{ param.description }}{% else %} OpenAPI parameter corresponding to '{{ param.name }}'{% endif %}
    {% endfor %}

    Returns:
        Any: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    logger.debug("Making {{ func.method.upper() }} request to {{ path }}")

    params = {}
    data = {}
    {% for param in func.params_info %}
        {%- if param.name.startswith("param_") %}
    if {{ param.name }} is not None:
        params["{{ param.name[6:] }}"] = (str({{ param.name }}).lower() if isinstance({{ param.name }}, bool) else {{ param.name }})
        {%- endif %}
    {% endfor %}

    flat_body = {}
    {%- for param in func.params %}
        {%- set param_name = param.split(':')[0] | trim %}
        {%- if param_name.startswith("body_") %}
    if {{ param_name }} is not None:
        flat_body["{{ param_name[5:] }}"] = {{ param_name }}
        {%- endif %}
    {%- endfor %}
    data = assemble_nested_body(flat_body)

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
