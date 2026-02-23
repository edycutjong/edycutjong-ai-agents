from agent.generator import DesignGenerator
from agent.models import TokenSet, DesignToken
import json

def test_to_css(sample_tokens):
    css = DesignGenerator.to_css(sample_tokens)
    assert ":root {" in css
    assert "--primary-500: #3B82F6;" in css
    assert "--spacing-md: 16px;" in css

def test_to_scss(sample_tokens):
    scss = DesignGenerator.to_scss(sample_tokens)
    assert "$primary-500: #3B82F6;" in scss
    assert "$spacing-md: 16px;" in scss

def test_to_tailwind(sample_tokens):
    tw = DesignGenerator.to_tailwind(sample_tokens)
    assert "module.exports =" in tw
    assert "colors" in tw
    assert '"primary-500": "#3B82F6"' in tw

def test_to_json(sample_tokens):
    json_str = DesignGenerator.to_json(sample_tokens)
    data = json.loads(json_str)
    assert data["primary-500"]["$value"] == "#3B82F6"
    assert data["primary-500"]["$type"] == "color"
