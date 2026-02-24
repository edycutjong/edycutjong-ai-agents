import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_review_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"style_issues": [], "bugs": [], "security_issues": [], "performance_tips": [], "complexity_rating": 3, "overall_quality": 8, "summary": "Clean code"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import CodeReviewAgent
    agent = CodeReviewAgent()
    result = agent.review("def hello(): pass")

    assert isinstance(result, dict)
    assert result["overall_quality"] == 8
    assert result["complexity_rating"] == 3
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_review_with_issues(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"style_issues": [{"line": 1, "issue": "no docstring", "suggestion": "add docstring"}], "bugs": [{"line": 5, "description": "null ref", "severity": "high"}], "security_issues": [], "performance_tips": ["use list comp"], "complexity_rating": 6, "overall_quality": 5, "summary": "Needs work"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import CodeReviewAgent
    agent = CodeReviewAgent()
    result = agent.review("x = eval(input())")

    assert len(result["style_issues"]) == 1
    assert result["bugs"][0]["severity"] == "high"
    assert result["overall_quality"] == 5
