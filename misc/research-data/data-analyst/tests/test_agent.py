import sys
import os
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

# Ensure we can import from the app directory
# Assuming the test is in apps/agents/data-analyst/tests/
# We want to add the app root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import load_data
from agent_config import create_agent

@pytest.fixture
def sample_csv(tmp_path):
    d = tmp_path / "data.csv"
    d.write_text("col1,col2\n1,a\n2,b")
    return str(d)

def test_load_data_csv(sample_csv):
    df = load_data(sample_csv)
    assert df is not None
    assert not df.empty
    assert list(df.columns) == ['col1', 'col2']
    assert len(df) == 2

def test_load_data_invalid_extension():
    # Helper to suppress stdout/stderr during test
    with patch('rich.console.Console.print'):
        df = load_data("test.txt")
    assert df is None

@patch('agent_config.ChatOpenAI')
@patch('agent_config.create_pandas_dataframe_agent')
def test_create_agent(mock_create_pandas_agent, mock_chat_openai):
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    mock_agent_executor = MagicMock()
    mock_create_pandas_agent.return_value = mock_agent_executor

    agent = create_agent(df)

    assert agent == mock_agent_executor
    mock_chat_openai.assert_called_once()
    mock_create_pandas_agent.assert_called_once()
