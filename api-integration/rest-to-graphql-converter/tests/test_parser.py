import sys
import os
import pytest
import yaml
import json

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.parser import OpenAPIParser

def test_parse_json_valid():
    content = '{"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0.0"}, "paths": {}}'
    parser = OpenAPIParser(content)
    info = parser.get_info()
    assert info["title"] == "Test API"

def test_parse_yaml_valid():
    content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths: {}
    """
    parser = OpenAPIParser(content)
    info = parser.get_info()
    assert info["title"] == "Test API"

def test_invalid_format():
    content = "invalid content"
    with pytest.raises(ValueError):
         OpenAPIParser(content)

def test_get_schemas():
    content = """
openapi: 3.0.0
components:
  schemas:
    User:
      type: object
    """
    parser = OpenAPIParser(content)
    schemas = parser.get_schemas()
    assert "User" in schemas

def test_summarize():
    content = """
    openapi: 3.0.0
    info:
      title: My API
      description: My Description
      version: 1.0.0
    paths:
      /users:
        get:
          summary: Get Users
    components:
      schemas:
        User:
          type: object
    """
    parser = OpenAPIParser(content)
    summary = parser.summarize()
    assert "API Title: My API" in summary
    assert "Description: My Description" in summary
    assert "GET /users: Get Users" in summary
    assert "User: object" in summary

def test_get_full_spec():
    content = '{"key": "value"}'
    parser = OpenAPIParser(content)
    assert parser.get_full_spec() == {"key": "value"}

def test_get_components_swagger_2():
    content = """
    swagger: "2.0"
    definitions:
      User:
        type: object
    """
    parser = OpenAPIParser(content)
    components = parser.get_components()
    assert "User" in components
    schemas = parser.get_schemas()
    assert "User" in schemas

def test_yaml_error():
    content = """
    invalid:
      - yaml: [
    """
    # This might raise YAMLError or ValueError depending on how pyyaml handles it.
    # The parser catches YAMLError and raises ValueError.
    with pytest.raises(ValueError, match="Invalid specification format"):
        OpenAPIParser(content)
