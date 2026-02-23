"""Tests for Postman to Code Converter."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import (
    parse_collection, convert_request, convert_collection,
    to_python, to_curl, to_javascript, to_go, ParsedRequest,
)

SAMPLE_COLLECTION = {
    "info": {"name": "Test API"},
    "item": [
        {
            "name": "Get Users",
            "request": {
                "method": "GET",
                "url": {"raw": "https://api.example.com/users"},
                "header": [{"key": "Accept", "value": "application/json"}],
            },
        },
        {
            "name": "Create User",
            "request": {
                "method": "POST",
                "url": "https://api.example.com/users",
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {"mode": "raw", "raw": '{"name": "John"}'},
                "auth": {"type": "bearer", "bearer": [{"key": "token", "value": "abc123"}]},
            },
        },
        {
            "name": "Folder",
            "item": [
                {
                    "name": "Nested",
                    "request": {"method": "DELETE", "url": "https://api.example.com/users/1"},
                },
            ],
        },
    ],
}

# --- Parsing ---
def test_parse_collection():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert len(reqs) == 3

def test_parse_method():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert reqs[0].method == "GET"
    assert reqs[1].method == "POST"

def test_parse_url():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert reqs[0].url == "https://api.example.com/users"

def test_parse_headers():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert reqs[0].headers["Accept"] == "application/json"

def test_parse_body():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert "John" in reqs[1].body

def test_parse_auth():
    reqs = parse_collection(SAMPLE_COLLECTION)
    assert reqs[1].auth_token == "abc123"

def test_parse_nested():
    reqs = parse_collection(SAMPLE_COLLECTION)
    nested = [r for r in reqs if r.method == "DELETE"]
    assert len(nested) == 1

# --- Python ---
def test_to_python():
    req = ParsedRequest(name="Test", method="GET", url="https://api.com/test")
    code = to_python(req)
    assert "requests.get" in code
    assert "https://api.com/test" in code

def test_python_with_auth():
    req = ParsedRequest(method="POST", url="https://api.com", auth_token="tok123")
    code = to_python(req)
    assert "Bearer tok123" in code

def test_python_with_body():
    req = ParsedRequest(method="POST", url="https://api.com", body='{"a":1}', body_type="raw")
    code = to_python(req)
    assert "data=" in code

# --- Curl ---
def test_to_curl():
    req = ParsedRequest(method="GET", url="https://api.com/test", headers={"Accept": "application/json"})
    code = to_curl(req)
    assert "curl -X GET" in code
    assert "Accept" in code

def test_curl_with_body():
    req = ParsedRequest(method="POST", url="https://api.com", body='{"a":1}')
    code = to_curl(req)
    assert "-d" in code

# --- JavaScript ---
def test_to_javascript():
    req = ParsedRequest(method="GET", url="https://api.com/test")
    code = to_javascript(req)
    assert "fetch" in code
    assert "https://api.com/test" in code

# --- Go ---
def test_to_go():
    req = ParsedRequest(method="GET", url="https://api.com/test")
    code = to_go(req)
    assert "http.NewRequest" in code
    assert "https://api.com/test" in code

# --- Collection ---
def test_convert_collection():
    code = convert_collection(SAMPLE_COLLECTION, "python")
    assert "requests.get" in code
    assert "requests.post" in code

def test_convert_collection_curl():
    code = convert_collection(SAMPLE_COLLECTION, "curl")
    assert "curl" in code

def test_unsupported_language():
    req = ParsedRequest(method="GET", url="https://api.com")
    code = convert_request(req, "rust")
    assert "Unsupported" in code

# --- Edge ---
def test_empty_collection():
    reqs = parse_collection({"item": []})
    assert len(reqs) == 0

def test_url_as_string():
    req = parse_collection({"item": [{"name": "T", "request": {"method": "GET", "url": "https://x.com"}}]})
    assert req[0].url == "https://x.com"
