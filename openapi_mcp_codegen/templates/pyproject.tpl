[project]
name = "{{ name }}"
version = "{{ version }}"
description = "{{ description }}"
license = "{{ license }}"
authors = [
  { name = "{{ author }}", email = "{{ email }}" }
]
readme = "README.md"

[tool.poetry.scripts]
mcp_argocd = "mcp_{{ mcp_name }}.server:main"

[tool.setuptools]
packages = ["mcp_{{ mcp_name }}"]

[tool.poetry.dependencies]
{{ poetry_dependencies }}
[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"