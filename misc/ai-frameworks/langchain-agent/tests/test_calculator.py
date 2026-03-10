import sys
import math
import pytest
from unittest.mock import MagicMock
import os

# Mock dependencies if they are not installed
if "langchain" not in sys.modules:
    sys.modules["langchain"] = MagicMock()
    sys.modules["langchain.tools"] = MagicMock()
if "langchain_community" not in sys.modules:
    sys.modules["langchain_community"] = MagicMock()
    sys.modules["langchain_community.tools"] = MagicMock()

# Import the function to test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.calculator import _safe_eval

def test_basic_math():
    assert _safe_eval("2 + 2") == "4"
    assert _safe_eval("15 * 23.5") == "352.5"
    assert _safe_eval("pow(2, 3)") == "8"
    assert _safe_eval("sqrt(144)") == "12.0"

def test_constants():
    assert float(_safe_eval("pi")) > 3.14
    assert float(_safe_eval("e")) > 2.71

def test_complex_expression():
    assert _safe_eval("2 * (3 + 4)") == "14"

def test_functions():
    assert _safe_eval("min(1, 2, 3)") == "1"
    assert _safe_eval("max(10, 2)") == "10"
    assert _safe_eval("abs(-5)") == "5"
    assert _safe_eval("round(3.14159, 2)") == "3.14"

def test_security_exploit_attempt():
    # Attempt to access internals
    payload = "(1).__class__.__base__.__subclasses__()"
    result = _safe_eval(payload)
    # The new implementation should return an error message caught by the try-except block
    # or raise ValueError which is then caught.
    assert "Error evaluating" in result
    result_lower = result.lower()
    allowed_errors = ["only direct function calls allowed", "unsupported", "not allowed", "error"]
    assert any(msg in result_lower for msg in allowed_errors)

def test_syntax_error():
    result = _safe_eval("2 + * 2")
    assert "Error evaluating" in result

def test_disallowed_names():
    result = _safe_eval("import os")
    assert "Error evaluating" in result

    result = _safe_eval("__import__('os')")
    assert "Error evaluating" in result
