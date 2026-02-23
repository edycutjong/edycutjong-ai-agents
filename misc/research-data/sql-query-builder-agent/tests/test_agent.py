import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
import os
import tempfile
from sqlalchemy import create_engine, text

# We need to add the parent directory to sys.path to import agent.sql_agent
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.sql_agent import SQLQueryBuilder

@pytest.fixture
def mock_chain():
    with patch("agent.sql_agent.create_sql_query_chain") as mock:
        yield mock

@pytest.fixture
def mock_chat_openai():
    with patch("agent.sql_agent.ChatOpenAI") as mock:
        yield mock

@pytest.fixture
def mock_sql_database():
    with patch("agent.sql_agent.SQLDatabase") as mock:
        mock_instance = MagicMock()
        mock.from_uri.return_value = mock_instance
        yield mock

def test_sql_agent_init(mock_chain, mock_chat_openai, mock_sql_database):
    agent = SQLQueryBuilder(api_key="test_key", db_uri="sqlite:///:memory:")
    assert agent.api_key == "test_key"
    mock_chain.assert_called_once()
    mock_chat_openai.assert_called_once()
    mock_sql_database.from_uri.assert_called_once_with("sqlite:///:memory:")

def test_generate_query(mock_chain, mock_chat_openai, mock_sql_database):
    mock_chain_instance = MagicMock()
    mock_chain.return_value = mock_chain_instance
    mock_chain_instance.invoke.return_value = "SELECT * FROM users"

    # We mock SQLQueryBuilder dependencies via fixtures
    agent = SQLQueryBuilder(api_key="test_key", db_uri="sqlite:///:memory:")
    query = agent.generate_query("Show me users")

    assert query == "SELECT * FROM users"
    mock_chain_instance.invoke.assert_called_once_with({"question": "Show me users"})

def test_validate_query(mock_chain, mock_chat_openai, mock_sql_database):
    agent = SQLQueryBuilder(api_key="test_key", db_uri="sqlite:///:memory:")
    assert agent.validate_query("SELECT * FROM users") == True
    assert agent.validate_query("INSERT INTO users (name) VALUES ('Alice')") == False
    assert agent.validate_query("UPDATE users SET name='Bob'") == False
    assert agent.validate_query("DELETE FROM users") == False
    assert agent.validate_query("DROP TABLE users") == False

def test_execute_query(mock_chain, mock_chat_openai):
    # We do NOT mock SQLDatabase here because we want to test real execution against a temporary DB.
    # But we mock ChatOpenAI and create_sql_query_chain to avoid LLM setup.

    # Create a temporary file db
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_uri_file = f"sqlite:///{db_path}"

    try:
        engine = create_engine(db_uri_file)
        with engine.connect() as conn:
            conn.execute(text("CREATE TABLE test (id INTEGER, name TEXT)"))
            conn.execute(text("INSERT INTO test VALUES (1, 'Alice')"))
            conn.commit()

        # We need to patch SQLDatabase.from_uri to NOT fail but return a real object?
        # Actually, since we are not mocking SQLDatabase fixture here, it uses the real class.
        # But wait, SQLDatabase from langchain might try to connect and inspect.
        # It requires `sqlalchemy`.

        agent = SQLQueryBuilder(api_key="test_key", db_uri=db_uri_file)

        # Verify execution
        df = agent.execute_query("SELECT * FROM test")

        assert not df.empty
        assert df.iloc[0]['name'] == 'Alice'
        assert len(df) == 1

    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
