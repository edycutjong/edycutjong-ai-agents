import sys
import os
import pytest
from unittest.mock import patch, MagicMock

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

def test_llm_engine_missing_api_key():
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = False
    
    with patch.multiple("config.config", OPENAI_API_KEY=""):
        engine = LLMEngine()
        assert engine.use_mock is True
        
    config.USE_MOCK_LLM = original_mock_setting

def test_llm_engine_real_llm_call():
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = False
    
    with patch.multiple("config.config", OPENAI_API_KEY="test_key"):
        with patch("agent.llm_engine.ChatOpenAI") as mock_openai:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value.content = "Real LLM response"
            mock_openai.return_value = mock_llm_instance
            
            engine = LLMEngine()
            response = engine.generate("System", "User")
            assert response == "Real LLM response"
            
    config.USE_MOCK_LLM = original_mock_setting

def test_llm_engine_real_llm_exception():
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = False
    
    with patch.multiple("config.config", OPENAI_API_KEY="test_key"):
        with patch("agent.llm_engine.ChatOpenAI") as mock_openai:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.side_effect = Exception("LLM Error")
            mock_openai.return_value = mock_llm_instance
            
            engine = LLMEngine()
            response = engine.generate("System", "User")
            assert "Error:" in response
            
    config.USE_MOCK_LLM = original_mock_setting

def test_llm_engine_mock_default():
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = True
    
    engine = LLMEngine()
    response = engine.generate("System: other", "User: other")
    assert "Mock response for testing." in response
    
    config.USE_MOCK_LLM = original_mock_setting

def test_llm_engine_mock_strategy():
    original_mock_setting = config.USE_MOCK_LLM
    config.USE_MOCK_LLM = True
    
    engine = LLMEngine()
    response = engine.generate("System: migration strategy", "User: Generate script")
    assert "RECOMMENDATION" in response
    
    config.USE_MOCK_LLM = original_mock_setting
