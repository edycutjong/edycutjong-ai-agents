import pytest
from unittest.mock import MagicMock, patch
from agent.generator import SOPGenerator
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_chat_openai():
    with patch('agent.generator.ChatOpenAI') as MockChatOpenAI:
        mock_instance = MagicMock()
        # Mock invoke method
        mock_instance.invoke.return_value = AIMessage(content="Mocked Response")
        # Mock __call__ method (for direct invocation)
        mock_instance.return_value = AIMessage(content="Mocked Response")
        MockChatOpenAI.return_value = mock_instance
        yield MockChatOpenAI

def test_generator_initialization(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    assert generator.api_key == "test_key"
    mock_chat_openai.assert_called_once()

def test_generate_title_metadata(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_title_metadata("Test Process")
    assert result == "Mocked Response"

def test_generate_purpose_scope(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_purpose_scope("Test Process", "Test Audience")
    assert result == "Mocked Response"

def test_generate_safety_compliance(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_safety_compliance("Test Process")
    assert result == "Mocked Response"

def test_generate_procedure_steps(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_procedure_steps("Test Process")
    assert result == "Mocked Response"

def test_generate_review_approval(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_review_approval()
    assert result == "Mocked Response"

def test_generate_full_sop(mock_chat_openai):
    generator = SOPGenerator(api_key="test_key")
    result = generator.generate_full_sop("Test Process")
    assert "Mocked Response" in result
