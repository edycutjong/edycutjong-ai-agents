import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_tailor_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"matched_keywords": ["Python", "API"], "missing_keywords": ["Kubernetes"], "skills_alignment": {"matched": ["Python"], "gaps": ["Kubernetes"]}, "experience_suggestions": [{"original": "Built APIs", "improved": "Designed and implemented RESTful APIs serving 1M+ requests/day"}], "ats_score": 72, "quality_score": 7, "summary": "Good match, add Kubernetes experience"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import ResumeTailorAgent
    agent = ResumeTailorAgent()
    result = agent.tailor("Python developer with API experience", "Looking for Python + Kubernetes engineer")

    assert isinstance(result, dict)
    assert result["ats_score"] == 72
    assert "Python" in result["matched_keywords"]
    assert "Kubernetes" in result["missing_keywords"]
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_tailor_strips_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"matched_keywords": [], "missing_keywords": ["Go"], "skills_alignment": {"matched": [], "gaps": ["Go"]}, "experience_suggestions": [], "ats_score": 30, "quality_score": 3, "summary": "Poor match"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import ResumeTailorAgent
    agent = ResumeTailorAgent()
    result = agent.tailor("JavaScript developer", "Go backend engineer")

    assert result["ats_score"] == 30
    assert "Go" in result["missing_keywords"]
