import sys
import os
import pytest

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.llm_engine import LLMEngine
from config import config

def test_llm_engine_mock_response():
    # Force use mock for test
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = True

    engine = LLMEngine()
    response = engine.generate("System: Mongo schema", "User: Generate schema")

    assert "collection" in response
    assert "users" in response

    # Reset config
    config.USE_MOCK_LLM = original_mock_setting

def test_llm_engine_dynamo_mock():
    # Force use mock for test
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = True

    engine = LLMEngine()
    response = engine.generate("System: DynamoDB table", "User: Generate table")

    assert "TableName" in response
    assert "KeySchema" in response

    # Reset config
    config.USE_MOCK_LLM = original_mock_setting
