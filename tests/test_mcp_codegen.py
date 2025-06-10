
import os
import shutil
import tempfile
import pytest
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

def test_camel_to_snake():
    from openapi_mcp_codegen.mcp_codegen import camel_to_snake
    assert camel_to_snake("CamelCase") == "camel_case"
    assert camel_to_snake("HTTPResponseCode") == "http_response_code"
    assert camel_to_snake("XYZ") == "x_y_z"

def test_resolve_ref(setup_env):
    gen = MCPGenerator(**setup_env)
    # Create a minimal dummy spec with a components/schemas section.
    gen.spec = {
        "components": {
            "schemas": {
                "TestModel": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"}
                    }
                }
            }
        }
    }
    ref = "#/components/schemas/TestModel"
    resolved = gen._resolve_ref(ref)
    assert resolved.get("type") == "object"
    assert "properties" in resolved

def test_extract_body_params_simple(setup_env):
    gen = MCPGenerator(**setup_env)
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name field"},
            "age": {"type": "integer"}
        },
        "required": ["name"]
    }
    params = gen._extract_body_params(schema, prefix="body")
    # Expect a required parameter for "name" and an optional one for "age"
    assert any("body_name: str" in p for p in params)
    assert any("body_age: int = None" in p for p in params)

def test_render_template_creates_file(setup_env):
    gen = MCPGenerator(**setup_env)
    # Create a temporary template in a new directory.
    import os
    from jinja2 import Environment, FileSystemLoader
    temp_template_dir = os.path.join(setup_env["output_dir"], "temp_templates")
    os.makedirs(temp_template_dir, exist_ok=True)
    template_file = os.path.join(temp_template_dir, "test.tpl")
    with open(template_file, "w", encoding="utf-8") as f:
        f.write("Hello, {{ name }}!")
    # Reset the Jinja2 environment to use our temporary template directory.
    gen.env = Environment(loader=FileSystemLoader(temp_template_dir))
    output_path = os.path.join(setup_env["output_dir"], "output.txt")
    gen.render_template("test.tpl", output_path, name="World")
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "Hello, World!"

def test_enhance_docstring_with_llm_dummy(setup_env, monkeypatch):
    gen = MCPGenerator(**setup_env, enhance_docstring_with_llm=True)
    # Create a dummy Python file with a simple async function.
    dummy_file = os.path.join(setup_env["output_dir"], "dummy.py")
    dummy_content = '''
async def tester(arg1: int):
    """Old docstring"""
    pass
'''
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write(dummy_content)
    # Monkey-patch LLMFactory so that get_llm().invoke returns a static docstring.
    class DummyLLM:
        def invoke(self, messages):
            class DummyResponse:
                content = '"""Enhanced docstring for tester"""'
            return DummyResponse()
    monkeypatch.setattr("cnoe_agent_utils.LLMFactory", lambda: type("Dummy", (), {"get_llm": lambda self: DummyLLM()})())
    output_dummy_file = os.path.join(setup_env["output_dir"], "dummy_enhanced.py")
    gen.enhance_docstring_with_llm(dummy_file, output_dummy_file, dry_run=False)
    with open(output_dummy_file, "r", encoding="utf-8") as f:
        enhanced_content = f.read()
    assert "Enhanced docstring for tester" in enhanced_content

def test_run_ruff_lint(monkeypatch, setup_env):
    gen = MCPGenerator(**setup_env)
    dummy_file = os.path.join(setup_env["output_dir"], "dummy.txt")
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write("print('Hello')")
    calls = []
    def fake_run(args, check):
        calls.append(args)
    monkeypatch.setattr("subprocess.run", fake_run)
    gen.run_ruff_lint(dummy_file)
    # Verify that at least one call to "ruff" was made.
    assert any("ruff" in arg for call in calls for arg in call)

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

def test_tool_parameter_descriptions(setup_env):
    from openapi_mcp_codegen.mcp_codegen import MCPGenerator
    import os

    # Instantiate the generator and generate tool modules.
    gen = MCPGenerator(**setup_env)
    gen.generate_tool_modules()

    # Determine the expected module file name for the /pet/findByStatus path.
    # The module name is created by stripping '/' and replacing separators,
    # so "/pet/findByStatus" becomes "pet_findbystatus.py"
    tools_dir = os.path.join(gen.src_output_dir, "tools")
    module_file = os.path.join(tools_dir, "pet_findbystatus.py")

    assert os.path.exists(module_file), f"Expected file {module_file} does not exist"

    with open(module_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify that the parameter description from the spec appears in the docstring.
    # For example, the query parameter 'status' in the /pet/findByStatus path
    # has the description "Status values that need to be considered for filter"
    assert "Status values that need to be considered for filter" in content, \
        "Parameter description not found in the function docstring"
