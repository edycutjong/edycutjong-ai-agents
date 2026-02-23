import os
import sys
import pytest
from unittest.mock import MagicMock

# Ensure the parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from agent.parser import get_language_from_extension, read_file_content, parse_uploaded_file

def test_get_language_from_extension():
    assert get_language_from_extension("component.js") == "javascript"
    assert get_language_from_extension("component.jsx") == "react"
    assert get_language_from_extension("component.ts") == "typescript"
    assert get_language_from_extension("component.tsx") == "react-ts"
    assert get_language_from_extension("component.vue") == "vue"
    assert get_language_from_extension("component.svelte") == "svelte"
    assert get_language_from_extension("template.html") == "angular-template"
    assert get_language_from_extension("unknown.xyz") == "text"
    assert get_language_from_extension("COMPONENT.JSX") == "react"

def test_read_file_content(tmp_path):
    # Create a temporary file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content", encoding="utf-8")

    content = read_file_content(str(p))
    assert content == "content"

def test_read_file_content_error():
    with pytest.raises(ValueError):
        read_file_content("non_existent_file.txt")

def test_parse_uploaded_file():
    # Mock Streamlit UploadedFile
    mock_file = MagicMock()
    mock_file.name = "Button.tsx"
    mock_file.getvalue.return_value = b"import React from 'react';"

    content, language = parse_uploaded_file(mock_file)

    assert content == "import React from 'react';"
    assert language == "react-ts"
