import json
import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_translate_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"greeting": "Hola", "farewell": "Adiós", "welcome": "Bienvenido, {{name}}"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import I18nTranslatorAgent
    agent = I18nTranslatorAgent()
    source = json.dumps({"greeting": "Hello", "farewell": "Goodbye", "welcome": "Welcome, {{name}}"})
    result = agent.translate(source, "Spanish")

    assert isinstance(result, dict)
    assert result["greeting"] == "Hola"
    assert "{{name}}" in result["welcome"]
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_translate_strips_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"hello": "こんにちは"}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import I18nTranslatorAgent
    agent = I18nTranslatorAgent()
    result = agent.translate('{"hello": "Hello"}', "Japanese")

    assert result["hello"] == "こんにちは"


@patch("src.agent.genai")
def test_review_quality(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"quality_score": 9, "issues": [], "placeholder_errors": [], "summary": "Excellent translation"}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import I18nTranslatorAgent
    agent = I18nTranslatorAgent()
    result = agent.review_quality('{"hi": "Hello"}', '{"hi": "Hola"}', "English", "Spanish")

    assert result["quality_score"] == 9
    assert len(result["issues"]) == 0
