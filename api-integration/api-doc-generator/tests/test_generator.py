"""Tests for API Doc Generator."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import parse_flask_routes, parse_express_routes, parse_fastapi_routes, detect_framework, generate_openapi, generate_markdown_docs

FLASK_CODE = '''
from flask import Flask
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users."""
    return []

@app.route('/users/<user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    """Get or delete a user."""
    pass

@app.route('/posts', methods=['POST'])
def create_post():
    pass
'''

EXPRESS_CODE = '''
const express = require('express');
const app = express();
app.get('/api/users', handler);
app.post('/api/users', handler);
app.get('/api/users/:id', handler);
app.delete('/api/users/:id', handler);
'''

FASTAPI_CODE = '''
from fastapi import FastAPI
app = FastAPI()

@app.get("/items")
def list_items(): pass

@app.post("/items")
def create_item(): pass

@app.get("/items/{item_id}")
def get_item(item_id: str): pass
'''

# --- Flask ---
def test_parse_flask():
    eps = parse_flask_routes(FLASK_CODE)
    assert len(eps) >= 3

def test_flask_methods():
    eps = parse_flask_routes(FLASK_CODE)
    methods = [e.method for e in eps]
    assert "GET" in methods
    assert "POST" in methods

def test_flask_docstring():
    eps = parse_flask_routes(FLASK_CODE)
    users_ep = next(e for e in eps if e.path == "/users" and e.method == "GET")
    assert "users" in users_ep.description.lower() or users_ep.summary

def test_flask_params():
    eps = parse_flask_routes(FLASK_CODE)
    user_ep = next(e for e in eps if "user_id" in str(e.parameters))
    assert len(user_ep.parameters) >= 1

# --- Express ---
def test_parse_express():
    eps = parse_express_routes(EXPRESS_CODE)
    assert len(eps) == 4

def test_express_path_params():
    eps = parse_express_routes(EXPRESS_CODE)
    param_eps = [e for e in eps if e.parameters]
    assert len(param_eps) >= 1

# --- FastAPI ---
def test_parse_fastapi():
    eps = parse_fastapi_routes(FASTAPI_CODE)
    assert len(eps) == 3

def test_fastapi_params():
    eps = parse_fastapi_routes(FASTAPI_CODE)
    item_ep = next(e for e in eps if "item_id" in str(e.parameters))
    assert len(item_ep.parameters) >= 1

# --- Detection ---
def test_detect_flask():
    assert detect_framework(FLASK_CODE) == "flask"

def test_detect_express():
    assert detect_framework(EXPRESS_CODE) == "express"

def test_detect_fastapi():
    assert detect_framework(FASTAPI_CODE) == "fastapi"

# --- OpenAPI ---
def test_openapi_structure():
    eps = parse_flask_routes(FLASK_CODE)
    spec = generate_openapi(eps, title="Test API")
    assert spec["openapi"] == "3.0.0"
    assert spec["info"]["title"] == "Test API"
    assert "/users" in spec["paths"]

def test_openapi_methods():
    eps = parse_flask_routes(FLASK_CODE)
    spec = generate_openapi(eps)
    assert "get" in spec["paths"]["/users"]

# --- Markdown ---
def test_markdown_output():
    eps = parse_flask_routes(FLASK_CODE)
    md = generate_markdown_docs(eps, title="My API")
    assert "My API" in md
    assert "`GET`" in md

def test_markdown_params():
    eps = parse_flask_routes(FLASK_CODE)
    md = generate_markdown_docs(eps)
    assert "user_id" in md

# --- Edge ---
def test_empty_code():
    assert len(parse_flask_routes("")) == 0
    assert len(parse_express_routes("")) == 0
    assert len(parse_fastapi_routes("")) == 0
