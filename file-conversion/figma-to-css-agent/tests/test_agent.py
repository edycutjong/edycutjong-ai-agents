import pytest
from agent.tools import convert_figma_to_css, parse_figma_structure
import json
import os

@pytest.fixture
def sample_json():
    path = os.path.join(os.path.dirname(__file__), "data/mock_figma.json")
    with open(path, "r") as f:
        return f.read()

def test_tool_convert_css(sample_json):
    result = convert_figma_to_css.invoke({"json_content": sample_json, "format": "css"})
    assert ".My-Button" in result
    assert "background-color" in result

def test_tool_convert_scss(sample_json):
    result = convert_figma_to_css.invoke({"json_content": sample_json, "format": "scss"})
    assert ".My-Button" in result

def test_tool_convert_css_in_js(sample_json):
    result = convert_figma_to_css.invoke({"json_content": sample_json, "format": "css-in-js"})
    assert "export const MyButton" in result

def test_tool_structure(sample_json):
    result = parse_figma_structure.invoke({"json_content": sample_json})
    assert "My Button (FRAME)" in result
    assert "Label (TEXT)" in result
