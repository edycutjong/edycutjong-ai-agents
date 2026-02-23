import pytest
from unittest.mock import MagicMock
from agent.tools import (
    research_tool,
    calculator_tool,
    accommodation_tool,
    dining_tool,
)

def test_calculator_tool_valid():
    result = calculator_tool.invoke({"expression": "2 + 2"})
    assert result == "4"

def test_calculator_tool_invalid():
    result = calculator_tool.invoke({"expression": "invalid expression"})
    assert "Error calculating" in result

def test_research_tool_mock(mocker):
    mock_run = MagicMock()
    mock_run.invoke.return_value = "Search Results"
    mocker.patch("agent.tools.search_run", mock_run)

    result = research_tool.invoke({"query": "Paris"})
    assert result == "Search Results"
    mock_run.invoke.assert_called_with("Paris")

def test_research_tool_error(mocker):
    mock_run = MagicMock()
    mock_run.invoke.side_effect = Exception("Search failed")
    mocker.patch("agent.tools.search_run", mock_run)

    result = research_tool.invoke({"query": "Paris"})
    assert "Error performing search" in result

def test_accommodation_tool_mock(mocker):
    mock_run = MagicMock()
    mock_run.invoke.return_value = "Hotel Mock"
    mocker.patch("agent.tools.search_run", mock_run)

    result = accommodation_tool.invoke({"query": "Tokyo"})
    assert result == "Hotel Mock"
    mock_run.invoke.assert_called_with("accommodation hotels Tokyo")

def test_dining_tool_mock(mocker):
    mock_run = MagicMock()
    mock_run.invoke.return_value = "Restaurant Mock"
    mocker.patch("agent.tools.search_run", mock_run)

    result = dining_tool.invoke({"query": "Rome"})
    assert result == "Restaurant Mock"
    mock_run.invoke.assert_called_with("restaurants dining Rome")
