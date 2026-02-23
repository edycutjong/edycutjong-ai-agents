import pytest
from agent.analyzer import analyze_code_structure

def test_analyze_code_structure_valid():
    code = """
class MyClass:
    '''Class docstring'''
    def my_method(self, arg1):
        '''Method docstring'''
        pass

def my_function(arg2):
    '''Function docstring'''
    pass
"""
    structure = analyze_code_structure(code)

    assert "classes" in structure
    assert "functions" in structure
    assert "MyClass" in structure["classes"]
    assert structure["classes"]["MyClass"]["docstring"] == "Class docstring"
    assert "my_method" in structure["classes"]["MyClass"]["methods"]
    assert "my_function" in structure["functions"]

def test_analyze_code_structure_invalid():
    code = "def invalid_syntax("
    structure = analyze_code_structure(code)
    assert "error" in structure
