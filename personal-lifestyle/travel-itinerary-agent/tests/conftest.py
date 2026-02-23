import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_search_tool():
    tool = MagicMock()
    tool.invoke.return_value = "Mock search results"
    return tool

@pytest.fixture
def mock_llm_chain():
    chain = MagicMock()
    chain.invoke.return_value = {"output": "Mock Itinerary"}
    return chain
