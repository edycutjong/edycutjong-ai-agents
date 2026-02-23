import pytest
from unittest.mock import MagicMock
import sys
import os

# Add package root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def mock_llm_response():
    mock = MagicMock()
    mock.invoke.return_value.content = "Mocked LLM Response"
    return mock

@pytest.fixture
def mock_requests_get(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("requests.get", mock)
    return mock
