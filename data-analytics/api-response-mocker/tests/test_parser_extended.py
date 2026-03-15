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

def test_parser_response_schema_invalid_int_cast():
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
    assert parser.get_response_schema('/test', 'GET', status_code='invalid')['type'] == 'integer'

def test_parser_response_schema_no_response():
    from unittest.mock import patch, PropertyMock
    # Test the code path where no response matches (line 59-60 in parser.py)
    spec = """
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
          content:
            application/json:
              schema:
                type: string
    """
    parser = OpenAPIParser(spec)
    # Ask for status_code '999' which won't match any response,
    # AND won't match 'default', AND has no 2xx fallback either
    # But our spec has '200' which starts with '2', so it will match the 2xx fallback
    # To hit line 60, we need an operation with responses that have NO 2xx codes and no default
    # We'll mock the specification to achieve this
    with patch.object(type(parser), 'specification', new_callable=PropertyMock) as mock_spec:
        mock_spec.return_value = {
            'paths': {
                '/test': {
                    'get': {
                        'responses': {
                            '500': {'description': 'Error'}
                        }
                    }
                }
            }
        }
        result = parser.get_response_schema('/test', 'GET', status_code='999')
        assert result is None

def test_parser_response_schema_content_fallback():
    spec = """
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
          content:
            text/plain:
              schema:
                type: string
    """
    parser = OpenAPIParser(spec)
    assert parser.get_response_schema('/test', 'GET')['type'] == 'string'

def test_parser_response_schema_no_schema():
    spec = """
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
          content:
            application/json:
              example: "value"
    """
    parser = OpenAPIParser(spec)
    assert parser.get_response_schema('/test', 'GET') is None
