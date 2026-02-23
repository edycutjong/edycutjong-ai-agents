import pytest
from agent.parser import OpenAPIParser
import os
import yaml

def test_parser_init():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    parser = OpenAPIParser(spec_content)
    assert parser.specification['info']['title'] == 'Sample API'

def test_get_paths():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    parser = OpenAPIParser(spec_content)
    paths = parser.get_paths()
    assert '/users' in paths
    assert '/users/{id}' in paths

def test_get_methods():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    parser = OpenAPIParser(spec_content)
    methods = parser.get_methods_for_path('/users')
    assert 'GET' in methods
    assert 'POST' not in methods

def test_get_response_schema():
    spec_path = os.path.join(os.path.dirname(__file__), 'sample_spec.yaml')
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    parser = OpenAPIParser(spec_content)
    schema = parser.get_response_schema('/users/{id}', 'GET')

    # Prance resolves references, so schema should contain actual properties
    assert schema['type'] == 'object'
    assert 'properties' in schema
    assert 'id' in schema['properties']
    assert 'name' in schema['properties']
