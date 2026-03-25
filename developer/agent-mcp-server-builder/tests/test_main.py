from main import run, parse_tool_description, generate_tool_schema, generate_project, format_preview


def test_run():
    assert "MCP Server Builder" in run("test")


def test_parse_tool():
    tools = parse_tool_description("search: Find documents\nanalyze: Analyze data")
    assert len(tools) == 2
    assert tools[0]["name"] == "search"


def test_parse_fallback():
    tools = parse_tool_description("just a phrase")
    assert len(tools) == 1


def test_empty_input():
    tools = parse_tool_description("")
    assert len(tools) == 1  # default hello_world


def test_schema():
    schema = generate_tool_schema({"name": "test", "description": "A test tool"})
    assert schema["name"] == "test"
    assert "inputSchema" in schema


def test_generate_project():
    tools = [{"name": "greet", "description": "Say hello"}]
    files = generate_project(tools, "test-server")
    assert "server.py" in files
    assert "README.md" in files


def test_preview():
    tools = [{"name": "fetch", "description": "Fetch data"}]
    preview = format_preview(tools, "my-server")
    assert "my-server" in preview
    assert "fetch" in preview
