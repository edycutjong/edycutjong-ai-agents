import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_triage_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"severity": "high", "component": "auth", "is_duplicate": false, "priority_score": 8, "suggested_assignee": "backend-team", "labels": ["bug", "auth"], "summary": "Login fails on timeout"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import BugTriageAgent
    agent = BugTriageAgent()
    result = agent.triage("Login page crashes after 30 seconds")

    assert isinstance(result, dict)
    assert result["severity"] == "high"
    assert result["priority_score"] == 8
    assert "auth" in result["labels"]
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_triage_strips_markdown_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"severity": "low", "component": "ui", "is_duplicate": false, "priority_score": 2, "suggested_assignee": "frontend", "labels": ["ui"], "summary": "Minor typo"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import BugTriageAgent
    agent = BugTriageAgent()
    result = agent.triage("Typo in button text")

    assert result["severity"] == "low"
    assert result["component"] == "ui"
