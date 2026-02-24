import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_summarize_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"title": "Sprint Planning", "date": "2024-01-15", "attendees": ["Alice", "Bob"], "key_points": ["Discussed sprint goals"], "action_items": [{"task": "Write tests", "assignee": "Bob", "deadline": "Friday"}], "decisions": ["Use pytest"], "follow_ups": ["Review next week"], "metadata": {"duration_mentioned": "1 hour", "meeting_type": "sprint"}, "summary": "Sprint planning meeting to set goals."}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import MeetingSummarizerAgent
    agent = MeetingSummarizerAgent()
    result = agent.summarize("Alice: Let's plan the sprint. Bob: Sure, I'll write the tests.")

    assert isinstance(result, dict)
    assert result["title"] == "Sprint Planning"
    assert len(result["action_items"]) == 1
    assert result["action_items"][0]["assignee"] == "Bob"
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_summarize_strips_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"title": "Standup", "date": "Unknown", "attendees": [], "key_points": ["Updates shared"], "action_items": [], "decisions": [], "follow_ups": [], "metadata": {}, "summary": "Quick standup."}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import MeetingSummarizerAgent
    agent = MeetingSummarizerAgent()
    result = agent.summarize("Quick standup update")

    assert result["title"] == "Standup"
    assert "Quick standup" in result["summary"]
