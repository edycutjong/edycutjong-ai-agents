import pytest
from unittest.mock import MagicMock, patch
from agent.llm_engine import LLMEngine
from config import Config

@patch('agent.llm_engine.Config.OPENAI_API_KEY', None)
@patch('agent.llm_engine.Config.GOOGLE_API_KEY', None)
def test_llm_engine_mock(sample_df):
    engine = LLMEngine()
    columns = {col: str(sample_df[col].dtype) for col in sample_df.columns}

    # Test line chart request
    result = engine.process_request(columns, "Show me a line chart of sales over time")
    assert result['chart_type'] == 'line'
    assert result['tool'] == 'python'

    # Test interactive chart request
    result = engine.process_request(columns, "Show me an interactive bar chart")
    assert result['chart_type'] == 'bar'
    assert result['tool'] == 'js'

@patch('agent.llm_engine.Config.OPENAI_API_KEY', 'fake_key')
@patch('agent.llm_engine.ChatOpenAI')
def test_llm_engine_openai(mock_chat_openai, sample_df):
    # This test verifies that if an API key is present, the LLM is initialized
    engine = LLMEngine()
    assert engine.llm is not None
    mock_chat_openai.assert_called()
