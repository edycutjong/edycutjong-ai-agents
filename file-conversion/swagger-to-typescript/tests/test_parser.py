import pytest
from unittest.mock import patch, MagicMock
from agent.parser import load_swagger
import tempfile
import os

def test_load_swagger_from_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"openapi": "3.0.0", "info": {"title": "Test", "version": "1.0.0"}}')
        path = f.name

    try:
        spec = load_swagger(path)
        assert spec["openapi"] == "3.0.0"
        assert spec["info"]["title"] == "Test"
    finally:
        os.remove(path)

def test_load_swagger_from_yaml_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('openapi: 3.0.0\ninfo:\n  title: Test\n  version: 1.0.0')
        path = f.name

    try:
        spec = load_swagger(path)
        assert spec["openapi"] == "3.0.0"
        assert spec["info"]["title"] == "Test"
    finally:
        os.remove(path)

@patch('agent.parser.httpx.get')
def test_load_swagger_from_url(mock_get):
    mock_response = MagicMock()
    mock_response.text = '{"openapi": "3.0.0", "info": {"title": "Test URL", "version": "1.0.0"}}'
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    spec = load_swagger("http://example.com/swagger.json")
    assert spec["openapi"] == "3.0.0"
    assert spec["info"]["title"] == "Test URL"
