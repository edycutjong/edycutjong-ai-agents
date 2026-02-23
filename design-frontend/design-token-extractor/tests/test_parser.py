from agent.parser import DesignParser
import pytest

def test_parse_json_valid():
    content = '{"colors": {"primary": "#000"}}'
    result = DesignParser.parse_content(content, "json")
    assert '"primary": "#000"' in result

def test_parse_json_invalid():
    content = '{"colors": '
    with pytest.raises(ValueError):
        DesignParser.parse_content(content, "json")

def test_parse_markdown():
    content = "# Colors\n- Primary: #000"
    result = DesignParser.parse_content(content, "md")
    assert result == content

def test_parse_text():
    content = "Primary: #000"
    result = DesignParser.parse_content(content, "txt")
    assert result == content
