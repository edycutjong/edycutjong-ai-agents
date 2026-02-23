"""Shared test fixtures for meeting-notes-organizer tests."""
import os
import sys
import json
import pytest
import tempfile

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

SAMPLE_TRANSCRIPT = """
John: Good morning everyone. Let's start with the sprint review.
Sarah: Sure. The API migration is 80% complete. I'll finish the remaining endpoints by Friday.
John: Great. Any blockers?
Mike: I need access to the staging database to run integration tests. Can someone set that up?
John: Sarah, can you help Mike with that today?
Sarah: Absolutely, I'll send him the credentials after this call.
John: Perfect. Let's also discuss the documentation. We need to update the API docs before release.
Mike: I can take that on. Should have it ready by next Wednesday.
John: Sounds good. Let's wrap up. Thanks everyone!
""".strip()

SAMPLE_ACTION_ITEMS = [
    {"task": "Finish API migration endpoints", "assignee": "Sarah", "priority": "High", "due_date": "Friday"},
    {"task": "Set up staging database access for Mike", "assignee": "Sarah", "priority": "High", "due_date": "today"},
    {"task": "Update API docs before release", "assignee": "Mike", "priority": "Medium", "due_date": "next Wednesday"},
]

SAMPLE_SPEAKERS = [
    {"name": "John", "role": "Meeting Lead", "topics": ["sprint review", "blockers", "documentation"], "talk_percentage": 40},
    {"name": "Sarah", "role": "Developer", "topics": ["API migration", "staging access"], "talk_percentage": 35},
    {"name": "Mike", "role": "Developer", "topics": ["integration tests", "API docs"], "talk_percentage": 25},
]

SAMPLE_SUMMARY = "Sprint review meeting covering API migration progress, staging database access, and documentation updates."

SAMPLE_RESULT = {
    "summary": SAMPLE_SUMMARY,
    "action_items": SAMPLE_ACTION_ITEMS,
    "speakers": SAMPLE_SPEAKERS,
    "email_draft": "Follow-up email draft here.",
}


@pytest.fixture
def sample_transcript():
    return SAMPLE_TRANSCRIPT


@pytest.fixture
def sample_result():
    return SAMPLE_RESULT


@pytest.fixture
def temp_storage_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "test_meetings.json")
