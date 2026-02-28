import pytest
import math
from tools.calculator import _safe_eval

def test_safe_eval_basic_math():
    assert _safe_eval("2 + 2") == "4"
    assert _safe_eval("10 - 5") == "5"
    assert _safe_eval("3 * 4") == "12"
    assert _safe_eval("15 / 3") == "5.0"
    assert _safe_eval("2 ** 3") == "8"

def test_safe_eval_functions():
    assert _safe_eval("abs(-10)") == "10"
    assert _safe_eval("round(3.14159, 2)") == "3.14"
    assert _safe_eval("min(1, 2, 3)") == "1"
    assert _safe_eval("max([1, 2, 3])") == "3"
    assert _safe_eval("sum([1, 2, 3, 4])") == "10"

def test_safe_eval_math_module():
    assert _safe_eval("sqrt(144)") == "12.0"
    assert _safe_eval("log(e)") == "1.0"

def test_safe_eval_malicious_code():
    result = _safe_eval('__import__("os").system("echo hacked")')
    assert "Error evaluating" in result

    result = _safe_eval('[].__class__.__bases__[0].__subclasses__()')
    assert "Error evaluating" in result

    result = _safe_eval('open("/etc/passwd", "r").read()')
    assert "Error evaluating" in result

    result = _safe_eval('eval("2 + 2")')
    assert "Error evaluating" in result
    assert "Name 'eval' is not allowed" in result
