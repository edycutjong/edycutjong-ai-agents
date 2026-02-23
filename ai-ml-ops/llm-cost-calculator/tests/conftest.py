"""Shared test fixtures for LLM Cost Calculator."""
import os
import sys
import pytest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.calculator import UsageEntry


@pytest.fixture
def sample_entries():
    """A batch of realistic usage entries."""
    return [
        UsageEntry(model="gpt-4o", input_tokens=5000, output_tokens=2000,
                   timestamp="2026-02-19T10:00:00", label="chat"),
        UsageEntry(model="gpt-4o", input_tokens=10000, output_tokens=3000,
                   timestamp="2026-02-19T11:00:00", label="summarization"),
        UsageEntry(model="claude-3.5-sonnet", input_tokens=8000, output_tokens=4000,
                   timestamp="2026-02-19T12:00:00", label="chat"),
        UsageEntry(model="gemini-2.0-flash", input_tokens=20000, output_tokens=5000,
                   timestamp="2026-02-19T13:00:00", label="analysis"),
        UsageEntry(model="gpt-4-turbo", input_tokens=3000, output_tokens=1000,
                   timestamp="2026-02-19T14:00:00", label="chat"),
    ]


@pytest.fixture
def temp_storage_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "test_usage.json")
