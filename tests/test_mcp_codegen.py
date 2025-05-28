
import os
import shutil
import tempfile
import pytest
import yaml
import json
from openapi_mcp_codegen.mcp_codegen import MCPGenerator

@pytest.fixture(scope="module")
def setup_env():
    """
    Sets up the environment for testing by preparing necessary directories and file paths.
    This function creates temporary directories and resolves paths for the example files,
    scripts, and configuration needed for testing. It yields a dictionary containing these
    paths for use in the test and ensures cleanup of the temporary directory after the test.
    Yields:
      dict: A dictionary containing the following keys:
        - script_dir (str): Path to the directory containing the templates/scripts.
        - output_dir (str): Path to the temporary output directory.
        - spec_path (str): Path to the OpenAPI specification file.
        - config_path (str): Path to the configuration file.
    Note:
      This test should be run from the root of the git repository to ensure correct resolution
      of file paths.
    """

    petstore_examples_dir = os.path.join(os.getcwd(), "examples", "petstore")
    script_dir = os.path.join(os.getcwd(), "openapi_mcp_codegen")
    output_dir = tempfile.mkdtemp()
    spec_path = os.path.join(petstore_examples_dir, "openapi_petstore.json")
    config_path = os.path.join(petstore_examples_dir, "config.yaml")

    print("========== Setup Environment ==========")
    print(f"petstore_examples_dir: {petstore_examples_dir}")
    print(f"script_dir: {script_dir}")
    print(f"output_dir: {output_dir}")
    print(f"spec_path: {spec_path}")
    print(f"config_path: {config_path}")
    print("========== End of Setup ==========")

    yield {
        "script_dir": script_dir,
        "output_dir": output_dir,
        "spec_path": spec_path,
        "config_path": config_path
    }
    shutil.rmtree(output_dir)

def test_generator_init(setup_env):
    gen = MCPGenerator(**setup_env)
    assert "info" in gen.spec
    assert gen.config["author"]

def test_get_python_type(setup_env):
    gen = MCPGenerator(**setup_env)
    assert gen._get_python_type({"type": "integer"}) == "int"
    assert gen._get_python_type({"type": "boolean"}) == "bool"
    assert gen._get_python_type({"type": "array", "items": {"type": "string"}}) == "List[str]"

def test_file_header_kwargs(setup_env):
    gen = MCPGenerator(**setup_env)
    headers = gen.get_file_header_kwargs()
    assert headers["file_headers"] is True
    assert isinstance(headers["file_headers_license"], str)

def test_generate_model_base(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_model_base()
    file_path = os.path.join(gen.src_output_dir, "models", "base.py")
    assert os.path.exists(file_path)

def test_generate_models(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_models()
    files = os.listdir(os.path.join(gen.src_output_dir, "models"))
    assert any(file.endswith(".py") and file != "base.py" for file in files)

def test_generate_api_client(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_api_client()
    assert os.path.exists(os.path.join(gen.src_output_dir, "api", "client.py"))

def test_generate_tool_modules(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_tool_modules()
    tool_dir = os.path.join(gen.src_output_dir, "tools")
    assert os.path.exists(tool_dir)
    assert any(file.endswith(".py") for file in os.listdir(tool_dir))

def test_generate_server(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_server()
    server_path = os.path.join(gen.src_output_dir, "server.py")
    assert os.path.exists(server_path)

def test_generate_readme(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_readme()
    assert os.path.exists(os.path.join(setup_env["output_dir"], "README.md"))

def test_generate_env(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_env()
    assert os.path.exists(os.path.join(setup_env["output_dir"], ".env.example"))

def test_generate_pyproject(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_pyproject()
    assert os.path.exists(os.path.join(setup_env["output_dir"], "pyproject.toml"))

def test_generate_init_files(setup_env):
    gen = MCPGenerator(**setup_env)
    gen.generate_init_files()
    assert os.path.exists(os.path.join(setup_env["output_dir"], "__init__.py"))
