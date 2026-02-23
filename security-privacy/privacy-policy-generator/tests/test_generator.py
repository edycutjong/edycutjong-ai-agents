import pytest
from unittest.mock import patch, MagicMock
from agent.generator import PolicyGenerator
from agent.formatter import PolicyFormatter

def test_formatter_markdown():
    text = "# Policy"
    assert PolicyFormatter.to_markdown(text) == text

def test_formatter_html():
    text = "# Policy\n\nContent"
    html = PolicyFormatter.to_html(text, title="Test Policy")
    assert "<!DOCTYPE html>" in html
    assert "<title>Test Policy</title>" in html
    assert "<h1>Policy</h1>" in html

@patch("agent.generator.ChatOpenAI")
def test_generator_init(mock_openai):
    gen = PolicyGenerator(api_key="test-key")
    mock_openai.assert_called_with(model="gpt-4-turbo", api_key="test-key")

@patch("agent.generator.ChatOpenAI")
@patch("agent.generator.ChatPromptTemplate")
@patch("agent.generator.StrOutputParser")
def test_generator_generate(mock_parser, mock_prompt, mock_openai):
    # Setup mocks
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Generated Policy"

    # Mocking the pipe behavior: prompt | llm | parser -> chain
    # This requires mocking the return values of each step to support __or__
    mock_prompt_instance = MagicMock()
    mock_prompt.from_messages.return_value = mock_prompt_instance

    mock_llm_instance = MagicMock()
    mock_openai.return_value = mock_llm_instance

    mock_parser_instance = MagicMock()
    mock_parser.return_value = mock_parser_instance

    # Chain: prompt | llm -> intermediate | parser -> chain
    mock_intermediate = MagicMock()
    mock_prompt_instance.__or__.return_value = mock_intermediate
    mock_intermediate.__or__.return_value = mock_chain

    gen = PolicyGenerator(api_key="test-key")

    scan_results = {"pii": ["email"], "third_parties": ["stripe"]}
    result = gen.generate_policy(scan_results, "gdpr")

    assert result == "Generated Policy"
    mock_chain.invoke.assert_called()
