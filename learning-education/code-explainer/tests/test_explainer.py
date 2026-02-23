"""Tests for Code Explainer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.explainer import detect_language, analyze_python, analyze_code, explain_code, CodeAnalysis

PY_CODE = '''
import os
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str

def greet(user):
    """Greet a user."""
    # Print greeting
    print(f"Hello, {user.name}")

async def fetch_data():
    pass
'''

JS_CODE = '''
const express = require("express");
function handleRequest(req, res) {
    console.log("Request received");
    res.json({ ok: true });
}
'''

def test_detect_python():
    assert detect_language(PY_CODE) == "python"

def test_detect_javascript():
    assert detect_language(JS_CODE) == "javascript"

def test_detect_html():
    assert detect_language("<html><head></head></html>") == "html"

def test_detect_sql():
    assert detect_language("SELECT * FROM users WHERE id = 1") == "sql"

def test_analyze_python_functions():
    a = analyze_python(PY_CODE)
    assert "greet" in a.functions

def test_analyze_python_async():
    a = analyze_python(PY_CODE)
    assert any("fetch_data" in f for f in a.functions)

def test_analyze_python_classes():
    a = analyze_python(PY_CODE)
    assert "User" in a.classes

def test_analyze_python_imports():
    a = analyze_python(PY_CODE)
    assert "os" in a.imports

def test_analyze_python_comments():
    a = analyze_python(PY_CODE)
    assert a.comments >= 1

def test_analyze_python_concepts():
    a = analyze_python(PY_CODE)
    assert "Decorators" in a.concepts

def test_complexity_low():
    a = analyze_python("x = 1")
    assert a.complexity == "low"

def test_complexity_high():
    code = "\n".join([f"if x{i}: pass" for i in range(15)])
    a = analyze_python(code)
    assert a.complexity == "high"

def test_analyze_code_auto():
    a = analyze_code(PY_CODE)
    assert a.language == "python"

def test_analyze_code_js():
    a = analyze_code(JS_CODE)
    assert a.language == "javascript"
    assert "handleRequest" in a.functions

def test_explain():
    md = explain_code(PY_CODE)
    assert "Code Analysis" in md
    assert "greet" in md

def test_to_dict():
    a = analyze_python(PY_CODE)
    d = a.to_dict()
    assert "language" in d and "functions" in d
