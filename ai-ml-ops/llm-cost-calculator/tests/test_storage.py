"""Tests for storage module."""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.storage import UsageStorage
from agent.calculator import UsageEntry


def test_add_and_retrieve(temp_storage_path):
    """Save an entry and retrieve it."""
    storage = UsageStorage(filepath=temp_storage_path)
    entry = UsageEntry(model="gpt-4o", input_tokens=1000, output_tokens=500,
                       timestamp="2026-01-01T00:00:00", label="test")
    storage.add_entry(entry)

    entries = storage.get_all_entries()
    assert len(entries) == 1
    assert entries[0].model == "gpt-4o"


def test_filter_by_model(temp_storage_path):
    """Filter entries by model name."""
    storage = UsageStorage(filepath=temp_storage_path)
    storage.add_entry(UsageEntry("gpt-4o", 100, 50, "2026-01-01T00:00:00"))
    storage.add_entry(UsageEntry("claude-3.5-sonnet", 200, 100, "2026-01-01T01:00:00"))
    storage.add_entry(UsageEntry("gpt-4o", 300, 150, "2026-01-01T02:00:00"))

    gpt_entries = storage.get_entries_by_model("gpt-4o")
    assert len(gpt_entries) == 2


def test_filter_by_label(temp_storage_path):
    """Filter entries by label."""
    storage = UsageStorage(filepath=temp_storage_path)
    storage.add_entry(UsageEntry("gpt-4o", 100, 50, "2026-01-01T00:00:00", "chat"))
    storage.add_entry(UsageEntry("gpt-4o", 200, 100, "2026-01-01T01:00:00", "analysis"))
    storage.add_entry(UsageEntry("gpt-4o", 300, 150, "2026-01-01T02:00:00", "chat"))

    chat = storage.get_entries_by_label("chat")
    assert len(chat) == 2


def test_clear_storage(temp_storage_path):
    """Clear removes all entries."""
    storage = UsageStorage(filepath=temp_storage_path)
    storage.add_entry(UsageEntry("gpt-4o", 100, 50, "2026-01-01T00:00:00"))
    storage.clear()
    assert len(storage.get_all_entries()) == 0


def test_empty_storage(temp_storage_path):
    """Empty storage returns empty list."""
    storage = UsageStorage(filepath=temp_storage_path)
    assert storage.get_all_entries() == []


def test_corrupted_json_recovery(temp_storage_path):
    """Recovers from corrupted storage file."""
    with open(temp_storage_path, "w") as f:
        f.write("not json!")

    storage = UsageStorage(filepath=temp_storage_path)
    assert storage.get_all_entries() == []
    # Can still add after recovery
    storage.add_entry(UsageEntry("gpt-4o", 100, 50, "2026-01-01T00:00:00"))
    assert len(storage.get_all_entries()) == 1
