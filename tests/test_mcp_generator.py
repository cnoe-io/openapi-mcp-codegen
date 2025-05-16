import os
import tempfile
import shutil
import json
import pytest
from openapi_mcp_codegen.mcp_codegen import MCPGenerator
import yaml

# test_mcp_codegen.py

@pytest.fixture
def minimal_openapi_spec():
  # Minimal OpenAPI spec for testing
  return {
    "openapi": "3.0.0",
    "info": {
      "title": "testapi",
      "version": "1.0.0"
    },
    "servers": [
      {"url": "https://api.example.com"}
    ],
    "paths": {
      "/items": {
        "get": {
          "operationId": "list_items",
          "summary": "List items",
          "description": "Returns a list of items."
        }
      }
    },
    "components": {
      "schemas": {
        "item": {
          "type": "object",
          "properties": {
            "id": {"type": "integer", "description": "Item ID"},
            "name": {"type": "string", "description": "Item name"}
          },
          "required": ["id"]
        }
      }
    }
  }

@pytest.fixture
def temp_output_dir():
  d = tempfile.mkdtemp()
  yield d
  shutil.rmtree(d)

def write_openapi_spec(spec, path):
  with open(path, "w", encoding="utf-8") as f:
    json.dump(spec, f)

def test_load_spec_json(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  assert gen.spec["info"]["title"] == "testapi"
  assert gen.base_path == "https://api.example.com"
  assert gen.mcp_name.startswith("testapi")
  print(f"Generated MCP name: {gen.mcp_name}")
  print(f"Generated MCP path: {gen.src_output_dir}")
  assert os.path.basename(gen.src_output_dir).startswith("mcp_testapi")

def test_load_spec_yaml(monkeypatch, minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.yaml")
  with open(spec_path, "w", encoding="utf-8") as f:
    yaml.safe_dump(minimal_openapi_spec, f)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  assert gen.spec["info"]["title"] == "testapi"

def test_create_directory_structure(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  for d in ["api", "models", "tools", "utils"]:
    assert os.path.isdir(os.path.join(gen.src_output_dir, d))

def test_generate_models_creates_files(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  gen.generate_models()
  base_model_path = os.path.join(gen.src_output_dir, "models", "base.py")
  item_model_path = os.path.join(gen.src_output_dir, "models", "item.py")
  assert os.path.isfile(base_model_path)
  assert os.path.isfile(item_model_path)
  with open(item_model_path, "r", encoding="utf-8") as f:
    code = f.read()
    assert "class Item(BaseModel):" in code

def test_get_python_type_handles_types():
  gen = MCPGenerator("dummy", "dummy")
  # integer
  assert gen._get_python_type({"type": "integer"}) == "int"
  # number
  assert gen._get_python_type({"type": "number"}) == "float"
  # boolean
  assert gen._get_python_type({"type": "boolean"}) == "bool"
  # array
  assert gen._get_python_type({"type": "array", "items": {"type": "string"}}) == "List[str]"
  # object
  assert gen._get_python_type({"type": "object"}) == "Dict"
  # default (string)
  assert gen._get_python_type({"type": "string"}) == "str"

def test_generate_api_client_creates_file(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  gen.generate_api_client()
  client_path = os.path.join(gen.src_output_dir, "api", "client.py")
  assert os.path.isfile(client_path)
  with open(client_path, "r", encoding="utf-8") as f:
    code = f.read()
    assert "async def make_api_request" in code

def test_generate_tool_module_creates_file(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  gen.generate_api_client()
  path = "/items"
  operations = minimal_openapi_spec["paths"][path]
  gen.generate_tool_module(path, operations)
  tool_path = os.path.join(gen.src_output_dir, "tools", "items.py")
  assert os.path.isfile(tool_path)
  with open(tool_path, "r", encoding="utf-8") as f:
    code = f.read()
    assert "async def list_items" in code

def test_generate_server_creates_file(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  gen.generate_api_client()
  gen.generate_tool_module("/items", minimal_openapi_spec["paths"]["/items"])
  gen.generate_server()
  server_path = os.path.join(gen.src_output_dir, "server.py")
  assert os.path.isfile(server_path)
  with open(server_path, "r", encoding="utf-8") as f:
    code = f.read()
    assert "def main()" in code

def test_generate_init_files_creates_files(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.create_directory_structure()
  gen.generate_init_files()
  for d in ["", "tools", "api", "models", "utils"]:
    init_path = os.path.join(gen.src_output_dir, d, "__init__.py") if d else os.path.join(gen.src_output_dir, "__init__.py")
    assert os.path.isfile(init_path)

def test_generate_pyproject_creates_file(minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.load_spec()
  gen.generate_pyproject()
  pyproject_path = os.path.join(temp_output_dir, "pyproject.toml")
  assert os.path.isfile(pyproject_path)
  with open(pyproject_path, "r", encoding="utf-8") as f:
    code = f.read()
    assert "[project]" in code

def test_generate_runs_all(monkeypatch, minimal_openapi_spec, temp_output_dir):
  spec_path = os.path.join(temp_output_dir, "openapi.json")
  write_openapi_spec(minimal_openapi_spec, spec_path)
  gen = MCPGenerator(spec_path, temp_output_dir)
  gen.generate()
  # Check some expected files
  assert os.path.isfile(os.path.join(gen.src_output_dir, "models", "item.py"))
  assert os.path.isfile(os.path.join(gen.src_output_dir, "api", "client.py"))
  assert os.path.isfile(os.path.join(gen.src_output_dir, "tools", "items.py"))
  assert os.path.isfile(os.path.join(gen.src_output_dir, "server.py"))
  assert os.path.isfile(os.path.join(temp_output_dir, "pyproject.toml"))
  assert os.path.isfile(os.path.join(temp_output_dir, ".env.example"))
  assert os.path.isfile(os.path.join(temp_output_dir, "README.md"))