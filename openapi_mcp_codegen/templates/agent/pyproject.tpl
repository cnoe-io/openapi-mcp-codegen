{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
[project]
name = "agent_{{ mcp_name }}"
version = "{{ version }}"
description = "{{ description }}"
license = "{{ license }}"
readme = "README.md"
authors = [
    { name = "{{ author }}", email = "{{ email }}" },
]
requires-python = ">=3.13,<4.0"
dependencies = [
{{ poetry_dependencies | indent(width=4) }}
]

[tool.hatch.build.targets.wheel]
# include every top-level package in the current directory
packages = ["."]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.poetry.scripts]
agent_{{ mcp_name }}_a2a = "protocol_bindings.a2a_server:main"

[tool.ruff]
line-length = 140
indent-width = 2

[tool.ruff.lint]
select = ["E", "F"]
ignore = ["F403"]

[tool.hatch.metadata]
allow-direct-references = true
