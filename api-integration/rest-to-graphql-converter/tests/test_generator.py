import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.generator import GraphQLGenerator

@pytest.fixture
def mock_openai(mocker):
    # Mock ChatOpenAI
    mock_llm = mocker.patch("agent.generator.ChatOpenAI")
    instance = mock_llm.return_value
    # Mock the invoke method which is called by the chain
    instance.invoke.return_value = MagicMock(content="Mocked GraphQL Content")
    return instance

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_generate_types(mock_openai):
    generator = GraphQLGenerator(api_key="test-key")

    # Mock the chain invocation
    with patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value="Mocked Types"):
        result = generator.generate_types({"User": {"type": "object"}}, "API Summary")
        assert result == "Mocked Types"

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_generate_operations(mock_openai):
    generator = GraphQLGenerator(api_key="test-key")

    with patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value="Mocked Operations"):
        result = generator.generate_operations({"path": "endpoint"}, "API Summary", "Existing Types")
        assert result == "Mocked Operations"

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_generate_resolvers(mock_openai):
    generator = GraphQLGenerator(api_key="test-key")

    with patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value="Mocked Resolvers"):
        result = generator.generate_resolvers("schema", "endpoints")
        assert result == "Mocked Resolvers"

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_generate_migration_guide(mock_openai):
    generator = GraphQLGenerator(api_key="test-key")

    with patch("langchain_core.runnables.base.RunnableSequence.invoke", return_value="Mocked Guide"):
        result = generator.generate_migration_guide("schema", "endpoints", "summary")
        assert result == "Mocked Guide"
