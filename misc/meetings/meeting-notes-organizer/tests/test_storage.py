"""Tests for MeetingStorage — all using temp files."""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.storage import MeetingStorage


def test_save_and_load(temp_storage_path):
    """Save a meeting and retrieve it from storage."""
    storage = MeetingStorage(filepath=temp_storage_path)
    mid = storage.save_meeting("transcript", "summary", [{"task": "t1"}], "email")

    meetings = storage.get_all_meetings()
    assert len(meetings) == 1
    assert meetings[0]["id"] == mid
    assert meetings[0]["transcript"] == "transcript"
    assert meetings[0]["summary"] == "summary"


def test_get_meeting_by_id(temp_storage_path):
    """Retrieve a specific meeting by its ID."""
    storage = MeetingStorage(filepath=temp_storage_path)
    mid = storage.save_meeting("t1", "s1", [], "e1")
    storage.save_meeting("t2", "s2", [], "e2")

    meeting = storage.get_meeting(mid)
    assert meeting is not None
    assert meeting["transcript"] == "t1"


def test_get_meeting_nonexistent(temp_storage_path):
    """Returns None for a nonexistent meeting ID."""
    storage = MeetingStorage(filepath=temp_storage_path)
    assert storage.get_meeting("nonexistent-id") is None


def test_empty_storage(temp_storage_path):
    """Empty storage returns empty list."""
    storage = MeetingStorage(filepath=temp_storage_path)
    assert storage.get_all_meetings() == []


def test_search_by_transcript(temp_storage_path):
    """Search matches text in transcripts."""
    storage = MeetingStorage(filepath=temp_storage_path)
    storage.save_meeting("alpha beta", "s1", [], "e1")
    storage.save_meeting("gamma delta", "s2", [], "e2")

    results = storage.search_meetings("alpha")
    assert len(results) == 1
    assert results[0]["transcript"] == "alpha beta"


def test_search_by_summary(temp_storage_path):
    """Search matches text in summaries."""
    storage = MeetingStorage(filepath=temp_storage_path)
    storage.save_meeting("t1", "important decision made", [], "e1")
    storage.save_meeting("t2", "routine standup", [], "e2")

    results = storage.search_meetings("important")
    assert len(results) == 1


def test_search_by_action_item(temp_storage_path):
    """Search matches text inside action item tasks."""
    storage = MeetingStorage(filepath=temp_storage_path)
    storage.save_meeting("t1", "s1", [{"task": "deploy to staging"}], "e1")
    storage.save_meeting("t2", "s2", [{"task": "fix bug"}], "e2")

    results = storage.search_meetings("deploy")
    assert len(results) == 1
    assert results[0]["action_items"][0]["task"] == "deploy to staging"


def test_corrupted_json_recovery(temp_storage_path):
    """Gracefully handles corrupted JSON file."""
    # Write invalid JSON
    with open(temp_storage_path, 'w') as f:
        f.write("{invalid json...")

    storage = MeetingStorage(filepath=temp_storage_path)
    meetings = storage.get_all_meetings()
    assert meetings == []

    # Should still be able to save after recovery
    mid = storage.save_meeting("t", "s", [], "e")
    assert len(storage.get_all_meetings()) == 1


def test_ordering_newest_first(temp_storage_path):
    """Meetings are returned newest first."""
    storage = MeetingStorage(filepath=temp_storage_path)
    storage.save_meeting("first", "s1", [], "e1")
    storage.save_meeting("second", "s2", [], "e2")

    meetings = storage.get_all_meetings()
    assert meetings[0]["transcript"] == "second"
    assert meetings[1]["transcript"] == "first"
