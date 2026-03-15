import os
import sys
import pytest
from unittest.mock import MagicMock

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
