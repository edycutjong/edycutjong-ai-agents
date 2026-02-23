import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from langchain_core.messages import AIMessage

# Add the application directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main import main
from utils import read_file
import agent_config

@pytest.fixture
def sample_txt_path():
    return os.path.join(os.path.dirname(__file__), 'sample_transcript.txt')

@pytest.fixture
def sample_vtt_path():
    return os.path.join(os.path.dirname(__file__), 'sample_transcript.vtt')

def test_read_txt(sample_txt_path):
    content = read_file(sample_txt_path)
    assert "Meeting Date: 2023-10-27" in content
    assert "Meeting adjourned." in content

def test_read_vtt(sample_vtt_path):
    content = read_file(sample_vtt_path)
    assert "Alice: Okay, let's get started." in content

@patch('agent_config.get_llm')
def test_chains(mock_get_llm):
    # Mock the LLM to return a predictable response
    mock_llm_instance = MagicMock()
    response = AIMessage(content="Mocked Response")

    # Mock invoke method
    mock_llm_instance.invoke.return_value = response
    # Mock __call__ method just in case
    mock_llm_instance.return_value = response

    mock_get_llm.return_value = mock_llm_instance

    # Test summary chain
    chain = agent_config.get_summary_chain()
    result = chain.invoke({"transcript": "test"})
    assert result == "Mocked Response"

    # Test other chains similarly
    chain = agent_config.get_action_items_chain()
    result = chain.invoke({"transcript": "test"})
    assert result == "Mocked Response"

@patch('main.get_summary_chain')
@patch('main.get_action_items_chain')
@patch('main.get_email_chain')
@patch('main.get_sentiment_chain')
def test_cli(mock_sentiment, mock_email, mock_action, mock_summary, sample_txt_path):
    # Mock chains to return simple strings
    # The chain.invoke method should return a string (since we use StrOutputParser)
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Mocked Result"

    mock_summary.return_value = mock_chain
    mock_action.return_value = mock_chain
    mock_email.return_value = mock_chain
    mock_sentiment.return_value = mock_chain

    runner = CliRunner()
    result = runner.invoke(main, [sample_txt_path])

    assert result.exit_code == 0
    # Check for non-ASCII-art parts of the UI
    assert "Analyze meeting transcripts with AI" in result.output
    assert "Analysis Complete!" in result.output
    # Check that our mocked result appears in the output
    assert "Mocked Result" in result.output
