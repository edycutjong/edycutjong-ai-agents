"""Tests for integrations: Jira, Calendar, email, and markdown export."""
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.integrations import (
    create_jira_issue,
    create_calendar_event,
    draft_followup_email,
    export_to_markdown,
)
from tests.conftest import SAMPLE_RESULT, SAMPLE_ACTION_ITEMS


def test_create_jira_issue_structure():
    """Jira mock returns proper response structure."""
    result = create_jira_issue("Fix bug", "Description")
    assert result["status"] == "success"
    assert result["key"].startswith("PROJ-")
    assert "message" in result


def test_create_calendar_event_structure():
    """Calendar mock returns proper response structure."""
    result = create_calendar_event("Standup", "Monday", "Daily standup")
    assert result["status"] == "success"
    assert result["event_id"].startswith("evt_")
    assert "Standup" in result["message"]


def test_draft_followup_email_with_items():
    """Email draft includes summary and action items."""
    email = draft_followup_email("Sprint review recap", SAMPLE_ACTION_ITEMS)
    assert "Sprint review recap" in email
    assert "Finish API migration" in email
    assert "Sarah" in email
    assert "Hi team" in email


def test_draft_followup_email_empty_items():
    """Email draft handles empty action items gracefully."""
    email = draft_followup_email("Quick sync", [])
    assert "Quick sync" in email
    assert "No action items" in email


def test_export_to_markdown_structure(sample_result):
    """Markdown export contains all expected sections."""
    md = export_to_markdown(sample_result)
    assert "# Meeting Notes" in md
    assert "## Summary" in md
    assert "## Speakers" in md
    assert "## Action Items" in md
    assert "John" in md
    assert "Sarah" in md


def test_export_to_markdown_with_transcript(sample_result):
    """Markdown export includes optional transcript in collapsible section."""
    md = export_to_markdown(sample_result, transcript="Raw transcript here")
    assert "<details>" in md
    assert "Raw transcript here" in md


def test_export_to_markdown_no_speakers():
    """Markdown export handles missing speakers gracefully."""
    result = {
        "summary": "Quick meeting",
        "action_items": [],
        "email_draft": "Email",
    }
    md = export_to_markdown(result)
    assert "## Summary" in md
    assert "## Speakers" not in md
    assert "No action items identified" in md


def test_export_to_markdown_action_table(sample_result):
    """Action items rendered as a markdown table."""
    md = export_to_markdown(sample_result)
    assert "| Task |" in md
    assert "| Finish API migration endpoints |" in md
