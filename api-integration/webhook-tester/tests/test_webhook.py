"""Tests for Webhook Tester storage and replay."""
import sys
import os
import json
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.storage import WebhookRequest, WebhookStorage
from agent.replay import generate_curl_command, generate_python_snippet


# --- Fixtures ---

@pytest.fixture
def temp_storage_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "test_webhooks.json")


@pytest.fixture
def sample_request():
    return WebhookRequest(
        method="POST",
        path="/api/webhook",
        headers={"Content-Type": "application/json", "X-Custom": "test"},
        body='{"event": "payment", "amount": 42.0}',
        content_type="application/json",
        source_ip="192.168.1.1",
    )


# --- WebhookRequest Tests ---

def test_request_auto_id():
    """Request gets auto-generated ID."""
    req = WebhookRequest(method="GET", path="/test")
    assert req.id
    assert len(req.id) == 8


def test_request_auto_timestamp():
    """Request gets auto-generated timestamp."""
    req = WebhookRequest(method="GET", path="/test")
    assert req.timestamp
    assert "T" in req.timestamp


def test_request_roundtrip():
    """Request serializes and deserializes."""
    req = WebhookRequest(method="POST", path="/hook", body="test data")
    d = req.to_dict()
    restored = WebhookRequest.from_dict(d)
    assert restored.method == "POST"
    assert restored.path == "/hook"
    assert restored.body == "test data"


def test_request_summary(sample_request):
    """Summary shows method, path, content type."""
    s = sample_request.summary()
    assert "POST" in s
    assert "/api/webhook" in s


# --- Storage Tests ---

def test_add_and_get_all(temp_storage_path, sample_request):
    """Store and retrieve requests."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(sample_request)
    requests = storage.get_all()
    assert len(requests) == 1
    assert requests[0].method == "POST"


def test_get_by_id(temp_storage_path, sample_request):
    """Retrieve by ID."""
    storage = WebhookStorage(filepath=temp_storage_path)
    req_id = storage.add(sample_request)
    result = storage.get_by_id(req_id)
    assert result is not None
    assert result.path == "/api/webhook"


def test_get_by_id_nonexistent(temp_storage_path):
    """Returns None for unknown ID."""
    storage = WebhookStorage(filepath=temp_storage_path)
    assert storage.get_by_id("fake-id") is None


def test_filter_by_method(temp_storage_path):
    """Filter by HTTP method."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(WebhookRequest(method="POST", path="/a"))
    storage.add(WebhookRequest(method="GET", path="/b"))
    storage.add(WebhookRequest(method="POST", path="/c"))

    posts = storage.filter_by_method("POST")
    assert len(posts) == 2
    gets = storage.filter_by_method("GET")
    assert len(gets) == 1


def test_filter_by_path(temp_storage_path):
    """Filter by path substring."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(WebhookRequest(method="POST", path="/api/v1/hook"))
    storage.add(WebhookRequest(method="POST", path="/api/v2/hook"))
    storage.add(WebhookRequest(method="POST", path="/health"))

    results = storage.filter_by_path("/api/")
    assert len(results) == 2


def test_clear(temp_storage_path, sample_request):
    """Clear removes all requests."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(sample_request)
    assert storage.count() == 1
    storage.clear()
    assert storage.count() == 0


def test_count(temp_storage_path):
    """Count returns correct number."""
    storage = WebhookStorage(filepath=temp_storage_path)
    assert storage.count() == 0
    storage.add(WebhookRequest(method="GET", path="/test"))
    assert storage.count() == 1


def test_export_json(temp_storage_path, sample_request):
    """JSON export is valid JSON."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(sample_request)
    exported = storage.export_json()
    parsed = json.loads(exported)
    assert len(parsed) == 1
    assert parsed[0]["method"] == "POST"


def test_export_markdown(temp_storage_path, sample_request):
    """Markdown export contains expected sections."""
    storage = WebhookStorage(filepath=temp_storage_path)
    storage.add(sample_request)
    md = storage.export_markdown()
    assert "# Webhook Capture Log" in md
    assert "POST /api/webhook" in md
    assert "X-Custom" in md


# --- Replay/Code Gen Tests ---

def test_generate_curl_command(sample_request):
    """Curl command includes method, headers, body."""
    cmd = generate_curl_command(sample_request, "https://example.com/hook")
    assert "curl -X POST" in cmd
    assert "X-Custom: test" in cmd
    assert "example.com/hook" in cmd
    assert "payment" in cmd


def test_generate_python_snippet(sample_request):
    """Python snippet is valid Python with requests lib."""
    snippet = generate_python_snippet(sample_request, "https://example.com/hook")
    assert "import requests" in snippet
    assert "requests.post" in snippet
    assert "example.com/hook" in snippet


def test_generate_curl_no_body():
    """Curl command for GET without body."""
    req = WebhookRequest(method="GET", path="/health")
    cmd = generate_curl_command(req)
    assert "curl -X GET" in cmd
    assert "-d" not in cmd


def test_corrupted_storage_recovery(temp_storage_path):
    """Recovers from corrupt JSON."""
    with open(temp_storage_path, "w") as f:
        f.write("{{broken}}")
    storage = WebhookStorage(filepath=temp_storage_path)
    assert storage.get_all() == []
    storage.add(WebhookRequest(method="GET", path="/test"))
    assert storage.count() == 1
