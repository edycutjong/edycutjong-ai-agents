import pytest
from agent.parser import OpenAPIParser

def test_parser_invalid_spec():
    with pytest.raises(ValueError):
        OpenAPIParser("invalid spec")

def test_parser_missing_paths():
    parser = OpenAPIParser("openapi: 3.0.0\ninfo:\n  title: Test\n  version: 1.0.0\npaths: {}")
    assert parser.get_paths() == []
    assert parser.get_response_schema('/missing', 'GET') is None

def test_parser_missing_methods():
    parser = OpenAPIParser("""
openapi: 3.0.0
info:
  title: Test
  version: 1.0.0
paths:
  /test:
    get:
      responses:
        '200':
          description: OK
""")
    assert 'GET' in parser.get_methods_for_path('/test')
    assert parser.get_response_schema('/test', 'POST') is None

def test_parser_response_schema_fallback():
    spec = """
openapi: 3.0.0
info:
  title: Test
  version: 1.0.0
paths:
  /test:
    get:
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                type: string
    """
    parser = OpenAPIParser(spec)
    # Default behavior: try 200, then 2xx
    assert parser.get_response_schema('/test', 'GET') is not None
    assert parser.get_response_schema('/test', 'GET')['type'] == 'string'

def test_parser_response_schema_default():
    spec = """
openapi: 3.0.0
info:
  title: Test
  version: 1.0.0
paths:
  /test:
    get:
      responses:
        default:
          description: Default
          content:
            application/json:
              schema:
                type: integer
    """
    parser = OpenAPIParser(spec)
    assert parser.get_response_schema('/test', 'GET')['type'] == 'integer'
