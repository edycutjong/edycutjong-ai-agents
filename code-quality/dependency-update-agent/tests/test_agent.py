import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_analyze_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"updates": [{"package": "requests", "current_version": "2.28.0", "latest_version": "2.31.0", "update_type": "minor", "risk_level": "low", "breaking_changes": false, "changelog_url": null}], "batch_plan": ["Update requests first"], "total_outdated": 1, "summary": "1 minor update available"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import DependencyUpdateAgent
    agent = DependencyUpdateAgent()
    result = agent.analyze("requests==2.28.0")

    assert isinstance(result, dict)
    assert result["total_outdated"] == 1
    assert len(result["updates"]) == 1
    assert result["updates"][0]["package"] == "requests"
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_analyze_with_breaking_changes(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"updates": [{"package": "django", "current_version": "3.2", "latest_version": "5.0", "update_type": "major", "risk_level": "high", "breaking_changes": true, "changelog_url": "https://docs.djangoproject.com/en/5.0/releases/"}], "batch_plan": ["Backup first", "Update django"], "total_outdated": 1, "summary": "Major update with breaking changes"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import DependencyUpdateAgent
    agent = DependencyUpdateAgent()
    result = agent.analyze("django==3.2")

    assert result["updates"][0]["breaking_changes"] is True
    assert result["updates"][0]["risk_level"] == "high"
