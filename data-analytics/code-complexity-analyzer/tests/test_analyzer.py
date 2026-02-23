"""Tests for Code Complexity Analyzer."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import calculate_complexity, detect_language, get_maintainability_index, format_result_markdown

PY_SIMPLE = "def foo():\n    return 1\n"
PY_COMPLEX = "def foo(x):\n    if x > 0:\n        for i in range(x):\n            if i % 2 == 0:\n                pass\n    elif x < 0:\n        pass\n    else:\n        pass\n"
JS_CODE = "function foo() {\n  if (x > 0) {\n    return true;\n  }\n  return false;\n}"

def test_lines(): r = calculate_complexity(PY_SIMPLE); assert r.total_lines >= 2
def test_complexity_simple(): r = calculate_complexity(PY_SIMPLE); assert r.cyclomatic_complexity == 1
def test_complexity_if(): r = calculate_complexity("if x:\n    pass\n"); assert r.cyclomatic_complexity >= 2
def test_complexity_multi(): r = calculate_complexity(PY_COMPLEX); assert r.cyclomatic_complexity >= 4
def test_grade_a(): r = calculate_complexity(PY_SIMPLE); assert r.grade == "A"
def test_grade_high():
    code = "\n".join(f"if x{i}:\n    pass" for i in range(20)); r = calculate_complexity(code); assert r.grade in ("C","D","F")
def test_blank_lines(): r = calculate_complexity("a = 1\n\nb = 2\n"); assert r.blank_lines >= 1
def test_comment_lines(): r = calculate_complexity("# comment\na = 1\n"); assert r.comment_lines == 1
def test_code_lines(): r = calculate_complexity(PY_SIMPLE); assert r.code_lines >= 1
def test_detect_python(): lang = detect_language(PY_SIMPLE); assert lang == "python"
def test_detect_js(): lang = detect_language(JS_CODE); assert lang == "javascript"
def test_functions(): r = calculate_complexity(PY_SIMPLE); assert any(f.name == "foo" for f in r.functions)
def test_function_params(): r = calculate_complexity("def bar(a, b, c):\n    pass\n"); assert r.functions[0].params == 3
def test_language_set(): r = calculate_complexity(PY_SIMPLE); assert r.language == "python"
def test_maintainability(): mi = get_maintainability_index(calculate_complexity(PY_SIMPLE)); assert mi > 0
def test_format(): md = format_result_markdown(calculate_complexity(PY_SIMPLE)); assert "Code Complexity" in md
def test_to_dict(): d = calculate_complexity(PY_SIMPLE).to_dict(); assert "complexity" in d
