import pytest
from tools.analyzer import CodeAnalyzer

def test_analyze_code_function():
    code = """
def hello(name):
    '''Says hello'''
    print(f"Hello {name}")
    """
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(code)

    assert "definitions" in result
    defs = result["definitions"]
    assert len(defs) == 1
    assert defs[0]["name"] == "hello"
    assert defs[0]["type"] == "FunctionDef"
    assert defs[0]["docstring"] == "Says hello"
    assert defs[0]["args"] == ["name"]

def test_analyze_code_class():
    code = """
class Greeter:
    '''Greeter class'''
    def greet(self):
        pass
    """
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_code(code)

    defs = result["definitions"]
    # Depending on implementation, might flatten or nest.
    # Current impl flattens all functions and classes
    assert len(defs) == 2 # Class and Method

    class_def = [d for d in defs if d["type"] == "ClassDef"][0]
    assert class_def["name"] == "Greeter"
    assert class_def["docstring"] == "Greeter class"

    method_def = [d for d in defs if d["type"] == "FunctionDef"][0]
    assert method_def["name"] == "greet"
