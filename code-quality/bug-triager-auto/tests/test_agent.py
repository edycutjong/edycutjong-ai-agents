import sys
import os
import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# Add app root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from agent.core import BugTriagerAgent
from agent.issue_tracker import IssueTracker
from config import Config

# Fixture for IssueTracker with temporary file
@pytest.fixture
def issue_tracker(tmp_path):
    # Use a temp file for data
    data_file = tmp_path / "test_data.json"
    tracker = IssueTracker(data_path=str(data_file))
    return tracker

@pytest.fixture
def agent(issue_tracker):
    # Force DEMO_MODE to avoid API calls, but we can also mock the LLM
    Config.DEMO_MODE = True
    return BugTriagerAgent(issue_tracker)

def test_add_issue(issue_tracker):
    issue = issue_tracker.add_issue("Test Bug", "This is a test bug description.")
    assert issue["title"] == "Test Bug"
    assert issue["status"] == "open"
    assert len(issue_tracker.get_all_issues()) == 1

def test_analyze_issue_mocked(agent, issue_tracker):
    # Create an issue
    issue = issue_tracker.add_issue("Crash in Login", "Login button causes crash.")

    # Run analysis (will use internal mocks since DEMO_MODE is True)
    updates = agent.analyze_issue(issue)

    updated_issue = issue_tracker.get_issue(issue["id"])

    assert updated_issue["severity"] in ["medium", "high", "critical", "low"]
    assert updated_issue["team"] in ["Backend", "Frontend", "Unassigned"]
    assert updated_issue["sentiment"] in ["positive", "neutral", "negative"]
    assert "AI Analysis" in updated_issue["analysis"]

def test_detect_duplicates(agent, issue_tracker):
    # Add an issue
    issue1 = issue_tracker.add_issue("Login Crash", "Application crashes when clicking login.")

    # Add a duplicate
    issue2 = {
        "id": "ISSUE-TEST",
        "title": "Login Crash",
        "description": "Application crashes when clicking login."
    }

    duplicates = agent.detect_duplicates(issue2)
    assert len(duplicates) == 1
    assert duplicates[0]["id"] == issue1["id"]

def test_check_stale_issues(agent, issue_tracker):
    # Add a stale issue manually
    old_date = (datetime.now() - timedelta(days=60)).isoformat()

    issue = issue_tracker.add_issue("Old Issue", "This is old.")
    # Manually update created_at
    issue["created_at"] = old_date
    issue_tracker.update_issue(issue["id"], {"created_at": old_date}) # Ensure it's saved

    count = agent.check_stale_issues(days_threshold=30)
    assert count == 1

    updated_issue = issue_tracker.get_issue(issue["id"])
    assert "stale" in updated_issue["labels"]

def test_suggest_fix(agent, issue_tracker):
    issue = issue_tracker.add_issue("Bug", "Desc")
    suggestion = agent.suggest_fix(issue["id"])

    assert "suggested_files" in suggestion
    assert "fix_strategy" in suggestion
