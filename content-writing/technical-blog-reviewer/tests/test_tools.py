import pytest
from unittest.mock import MagicMock
from agent.tools import extract_text_from_url, execute_python_snippet, extract_code_blocks, is_safe_code

def test_extract_text_from_url_success(mock_requests_get):
    mock_response = MagicMock()
    mock_response.content = b"<html><body><p>Hello World</p><script>alert('bad');</script></body></html>"
    mock_requests_get.return_value = mock_response

    text = extract_text_from_url("http://example.com")
    assert "Hello World" in text
    assert "alert" not in text

def test_extract_text_from_url_failure(mock_requests_get):
    mock_requests_get.side_effect = Exception("Connection Error")

    text = extract_text_from_url("http://example.com")
    assert "Error fetching URL" in text

def test_is_safe_code_safe():
    code = "print('Hello')"
    assert is_safe_code(code) is True

def test_is_safe_code_unsafe_import():
    code = "import os\nos.system('ls')"
    assert is_safe_code(code) is False

def test_is_safe_code_unsafe_from_import():
    code = "from subprocess import run"
    assert is_safe_code(code) is False

def test_is_safe_code_unsafe_builtin():
    code = "open('/etc/passwd')"
    assert is_safe_code(code) is False

def test_is_safe_code_unsafe_exec():
    code = "exec('print(1)')"
    assert is_safe_code(code) is False

def test_execute_python_snippet_success():
    code = "print('Hello Test')"
    result = execute_python_snippet(code)
    assert result["success"] is True
    assert "Hello Test" in result["stdout"]
    assert result["error"] is None

def test_execute_python_snippet_blocked():
    code = "import os\nprint('bad')"
    result = execute_python_snippet(code)
    assert result["success"] is False
    assert "Safety check failed" in result["error"]

def test_execute_python_snippet_failure():
    code = "raise ValueError('Test Error')"
    result = execute_python_snippet(code)
    assert result["success"] is False
    assert "Test Error" in result["error"]

def test_extract_code_blocks():
    content = """
    Here is code:
    ```python
    print('hello')
    ```
    And more:
    ```PYTHON
    x = 1
    ```
    """
    blocks = extract_code_blocks(content)
    assert len(blocks) == 2
    assert "print('hello')" in blocks[0]
    assert "x = 1" in blocks[1]

def test_is_safe_code_unsafe_attribute_access():
    code = "().__class__.__bases__[0].__subclasses__()"
    assert is_safe_code(code) is False

def test_is_safe_code_unsafe_globals():
    code = "print(globals())"
    assert is_safe_code(code) is False

def test_execute_python_snippet_no_object():
    code = "print(object)"
    result = execute_python_snippet(code)
    assert result["success"] is False
    assert "name 'object' is not defined" in result["error"]

def test_execute_python_snippet_no_type():
    code = "print(type(1))"
    result = execute_python_snippet(code)
    assert result["success"] is False
    assert "name 'type' is not defined" in result["error"]

def test_execute_python_snippet_blocked_reflection():
    code = "().__class__"
    result = execute_python_snippet(code)
    assert result["success"] is False
    assert "Safety check failed" in result["error"]
