import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Ensure the parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from agent.generator import ComponentDocumenter
from config import Config

@patch("agent.generator.ChatOpenAI")
def test_component_documenter_init(mock_chat_openai):
    # Test initialization with explicit API key
    doc = ComponentDocumenter(api_key="test_key")
    assert doc.api_key == "test_key"
    mock_chat_openai.assert_called_once()

@patch("agent.generator.ChatOpenAI")
def test_component_documenter_init_env(mock_chat_openai):
    # Test initialization with env variable via Config
    # We need to patch the Config class attribute
    with patch.object(Config, 'OPENAI_API_KEY', 'env_key'):
        doc = ComponentDocumenter()
        assert doc.api_key == "env_key"

@patch("agent.generator.ChatOpenAI")
def test_component_documenter_missing_key(mock_chat_openai):
    # Test initialization failure when no key is provided
    with patch.object(Config, 'OPENAI_API_KEY', None):
        with pytest.raises(ValueError, match="OpenAI API Key is required"):
            ComponentDocumenter(api_key=None)

@patch("agent.generator.ChatOpenAI")
def test_generate_documentation(mock_chat_openai):
    mock_response = MagicMock()
    mock_response.content = "# Documentation"

    doc = ComponentDocumenter(api_key="test")

    # Mock the chain's invoke method directly on the instance
    doc.chain = MagicMock()
    doc.chain.invoke.return_value = mock_response

    result = doc.generate_documentation("const A = () => {}", "react")

    assert result == "# Documentation"
    doc.chain.invoke.assert_called_once_with({
        "language": "react",
        "code": "const A = () => {}"
    })

@patch("agent.generator.ChatOpenAI")
def test_generate_documentation_error(mock_chat_openai):
    doc = ComponentDocumenter(api_key="test")
    doc.chain = MagicMock()
    doc.chain.invoke.side_effect = Exception("API Error")

    result = doc.generate_documentation("code", "react")

    assert "Error generating documentation: API Error" in result
