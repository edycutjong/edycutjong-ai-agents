import pytest
from unittest.mock import MagicMock
from agent.core import CopyEditorAgent, Config

@pytest.fixture
def mock_agent(mocker):
    mocker.patch.object(Config, 'OPENAI_API_KEY', 'fake-key')
    mocker.patch('agent.core.ChatOpenAI')
    return CopyEditorAgent(api_key="fake-key")

def test_agent_initialization_no_key(mocker):
    mocker.patch.object(Config, 'OPENAI_API_KEY', None)
    agent = CopyEditorAgent(api_key=None)
    assert agent.llm is None

def test_agent_initialization_with_key(mocker):
    mocker.patch('agent.core.ChatOpenAI')
    agent = CopyEditorAgent(api_key="test-key")
    assert agent.llm is not None

def test_edit_text_raises_error_without_key(mocker):
    mocker.patch.object(Config, 'OPENAI_API_KEY', None)
    agent = CopyEditorAgent(api_key=None)

    with pytest.raises(ValueError, match="OpenAI API Key is missing"):
        agent.edit_text("some text")

def test_edit_text_flow(mocker):
    """
    Tests that the chain is constructed and invoked.
    We mock the underlying components to ensure the flow is correct.
    """
    mocker.patch.object(Config, 'OPENAI_API_KEY', 'fake-key')

    # Mock ChatOpenAI
    mock_llm_class = mocker.patch('agent.core.ChatOpenAI')
    mock_llm_instance = mock_llm_class.return_value

    # Mock ChatPromptTemplate
    mock_prompt_cls = mocker.patch('agent.core.ChatPromptTemplate')
    mock_prompt_instance = mock_prompt_cls.from_template.return_value

    # Mock JsonOutputParser
    # Note: The agent instantiates this in __init__, so we need to mock the class before init or patch the instance on the agent.
    # Since we create agent inside test, we patch class before.
    mock_parser_cls = mocker.patch('agent.core.JsonOutputParser')
    mock_parser_instance = mock_parser_cls.return_value

    agent = CopyEditorAgent(api_key="fake-key")

    # Mock the chain construction via pipes
    # prompt | llm | parser
    # prompt.__or__(llm) -> intermediate
    # intermediate.__or__(parser) -> chain

    mock_intermediate = MagicMock()
    mock_chain = MagicMock()

    mock_prompt_instance.__or__.return_value = mock_intermediate
    mock_intermediate.__or__.return_value = mock_chain

    mock_chain.invoke.return_value = {
        "edited_text": "Edited Text",
        "summary_report": {}
    }

    # Run
    result = agent.edit_text("Original Text")

    # Verify
    assert result["edited_text"] == "Edited Text"
    mock_prompt_cls.from_template.assert_called_once()
    mock_chain.invoke.assert_called_once()
