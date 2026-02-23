from unittest.mock import MagicMock, patch
from agent.extractor import DesignTokenExtractor
from agent.generator import DesignGenerator
from agent.parser import DesignParser
from agent.models import TokenSet, DesignToken

@patch("agent.extractor.ChatOpenAI")
@patch("agent.extractor.ChatPromptTemplate")
def test_full_integration(MockPrompt, MockChatOpenAI):
    # Setup chain mock
    mock_llm = MockChatOpenAI.return_value
    mock_structured = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured

    # Mock the prompt | structured chain creation
    mock_chain = MagicMock()
    mock_prompt_instance = MockPrompt.from_messages.return_value
    mock_prompt_instance.__or__.return_value = mock_chain

    mock_token_set = TokenSet(
        name="test",
        tokens=[DesignToken(name="primary-500", value="#0000FF", type="color")]
    )
    mock_chain.invoke.return_value = mock_token_set

    # 1. Parse
    content = "Primary: #0000FF"
    parsed = DesignParser.parse_content(content, "md")

    # 2. Extract
    extractor = DesignTokenExtractor()
    tokens = extractor.extract(parsed)

    # 3. Generate
    css = DesignGenerator.to_css(tokens)

    assert "--primary-500: #0000FF;" in css
    assert ":root {" in css
