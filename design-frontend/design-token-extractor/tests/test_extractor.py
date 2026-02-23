from unittest.mock import MagicMock, patch
from agent.extractor import DesignTokenExtractor
from agent.models import TokenSet, DesignToken

@patch("agent.extractor.ChatOpenAI")
@patch("agent.extractor.ChatPromptTemplate")
def test_extractor_success(MockPrompt, MockChatOpenAI):
    # Setup mock
    mock_llm = MockChatOpenAI.return_value
    mock_structured = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured

    mock_chain = MagicMock()
    mock_prompt_instance = MockPrompt.from_messages.return_value
    mock_prompt_instance.__or__.return_value = mock_chain

    expected_tokens = TokenSet(
        name="test",
        tokens=[DesignToken(name="primary-500", value="#0000FF", type="color")]
    )
    mock_chain.invoke.return_value = expected_tokens

    extractor = DesignTokenExtractor()
    result = extractor.extract("some content")

    assert len(result.tokens) == 1
    assert result.tokens[0].name == "primary-500"
    mock_chain.invoke.assert_called_once()
