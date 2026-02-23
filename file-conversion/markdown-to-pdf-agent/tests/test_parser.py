import pytest
import os
from agent.parser import MarkdownParser

def test_parse_string():
    parser = MarkdownParser()
    text = "---\ntitle: Test\n---\n# Hello"
    res = parser.parse_string(text)
    assert res['metadata']['title'] == 'Test'
    assert '# Hello' in res['content']

def test_parse_file(tmp_path):
    parser = MarkdownParser()
    p = tmp_path / "test.md"
    p.write_text("---\nauthor: Me\n---\nHello World", encoding='utf-8')

    res = parser.parse_file(str(p))
    assert res['metadata']['author'] == 'Me'
    assert 'Hello World' in res['content']

def test_file_not_found():
    parser = MarkdownParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_file("non_existent_file.md")
