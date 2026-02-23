"""Tests for MeetingProcessor — all LLM calls are mocked."""
import sys
import os
import json
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.processor import MeetingProcessor
from tests.conftest import SAMPLE_ACTION_ITEMS, SAMPLE_SPEAKERS


@patch('agent.processor.ChatOpenAI')
def test_process_transcript_success(mock_openai, sample_transcript):
    """Full pipeline returns summary, action_items, speakers, and email_draft."""
    processor = MeetingProcessor(api_key="fake_key")
    processor._generate_summary = MagicMock(return_value="Summary text")
    processor._extract_action_items = MagicMock(return_value=SAMPLE_ACTION_ITEMS)
    processor._extract_speakers = MagicMock(return_value=SAMPLE_SPEAKERS)
    processor._draft_email = MagicMock(return_value="Email draft")

    result = processor.process_transcript(sample_transcript)

    assert result["summary"] == "Summary text"
    assert len(result["action_items"]) == 3
    assert len(result["speakers"]) == 3
    assert result["email_draft"] == "Email draft"
    assert "error" not in result


@patch('agent.processor.Config')
def test_process_transcript_no_api_key(mock_config):
    """Returns error dict when no API key is set."""
    mock_config.OPENAI_API_KEY = None
    mock_config.DEFAULT_MODEL = "gpt-4-turbo"
    processor = MeetingProcessor(api_key=None)
    result = processor.process_transcript("test transcript")
    assert "error" in result
    assert "API Key" in result["error"]


@patch('agent.processor.ChatOpenAI')
def test_process_transcript_exception_handling(mock_openai, sample_transcript):
    """Handles exceptions gracefully without crashing."""
    processor = MeetingProcessor(api_key="fake_key")
    processor._generate_summary = MagicMock(side_effect=RuntimeError("API down"))

    result = processor.process_transcript(sample_transcript)
    assert "error" in result
    assert "API down" in result["error"]


def test_parse_json_clean():
    """Parses clean JSON string."""
    data = json.dumps([{"task": "test"}])
    result = MeetingProcessor._parse_json_response(data)
    assert len(result) == 1
    assert result[0]["task"] == "test"


def test_parse_json_with_markdown_code_block():
    """Strips ```json ... ``` wrapper before parsing."""
    raw = '```json\n[{"task": "test"}]\n```'
    result = MeetingProcessor._parse_json_response(raw)
    assert len(result) == 1
    assert result[0]["task"] == "test"


def test_parse_json_with_plain_code_block():
    """Strips ``` ... ``` wrapper before parsing."""
    raw = '```\n[{"task": "test"}]\n```'
    result = MeetingProcessor._parse_json_response(raw)
    assert len(result) == 1


def test_parse_json_invalid_returns_empty():
    """Returns empty list on invalid JSON."""
    result = MeetingProcessor._parse_json_response("not json at all")
    assert result == []


@patch('agent.processor.ChatOpenAI')
def test_extract_speakers_returns_list(mock_openai, sample_transcript):
    """Speaker diarization returns a list of speaker dicts."""
    processor = MeetingProcessor(api_key="fake_key")
    processor._extract_speakers = MagicMock(return_value=SAMPLE_SPEAKERS)
    processor._generate_summary = MagicMock(return_value="Summary")
    processor._extract_action_items = MagicMock(return_value=[])
    processor._draft_email = MagicMock(return_value="Email")

    result = processor.process_transcript(sample_transcript)
    assert "speakers" in result
    assert isinstance(result["speakers"], list)
    assert result["speakers"][0]["name"] == "John"
