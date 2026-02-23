import pytest
from agent.parser import LogParser

def test_parser_initialization():
    parser = LogParser(api_key=None)
    # When no API key is set, llm may still initialize if OPENAI_API_KEY env var exists
    assert parser is not None

def test_mock_parser_valid_logs():
    parser = LogParser(api_key=None)
    raw_logs = "2023-10-27 INFO User login\n2023-10-27 ERROR Db fail"
    result = parser.parse(raw_logs)

    assert len(result) == 2
    assert result[0]['level'] == "INFO"
    assert result[1]['level'] == "ERROR"

def test_mock_parser_empty_logs():
    parser = LogParser(api_key=None)
    result = parser.parse("")
    assert result == []

def test_mock_parser_whitespace_logs():
    parser = LogParser(api_key=None)
    result = parser.parse("   \n   ")
    assert result == []
