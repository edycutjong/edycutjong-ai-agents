import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.generator import DocGenerator

@pytest.fixture
def mock_code_reader():
    with patch('agent.generator.CodeReader') as mock:
        yield mock

@pytest.fixture
def mock_llm_chain():
    # Patch the dependencies used in DocGenerator
    with patch('agent.generator.ChatOpenAI') as mock_llm_cls, \
         patch('agent.generator.PromptTemplate') as mock_prompt_cls, \
         patch('agent.generator.StrOutputParser') as mock_parser_cls:

        # Setup chain mocking
        mock_prompt_instance = mock_prompt_cls.from_template.return_value

        # prompt | llm -> intermediate
        mock_intermediate = MagicMock()
        mock_prompt_instance.__or__.return_value = mock_intermediate

        # intermediate | parser -> chain
        mock_chain = MagicMock()
        mock_intermediate.__or__.return_value = mock_chain

        # Chain invoke return value
        mock_chain.invoke.return_value = "Generated Documentation"

        yield mock_chain

def test_doc_generation(mock_code_reader, mock_llm_chain):
    mock_code_reader.read_file.return_value = "def hello(): pass"

    # We need to mock config as well if it's used in __init__
    with patch('agent.generator.config') as mock_config:
        mock_config.OPENAI_API_KEY = "sk-test"
        mock_config.DEFAULT_TONE = "Professional"
        mock_config.MODEL_NAME = "gpt-4-test"

        generator = DocGenerator()
        result = generator.generate_doc("test.py")

        assert result == "Generated Documentation"
        mock_code_reader.read_file.assert_called_with("test.py")
        mock_llm_chain.invoke.assert_called_once()

        # Check arguments passed to invoke
        # args[0] is the input dict to invoke
        args, kwargs = mock_llm_chain.invoke.call_args
        assert args[0]['code'] == "def hello(): pass"
        assert args[0]['filename'] == "test.py"
        assert args[0]['tone'] == "Professional"

def test_mermaid_generation(mock_code_reader, mock_llm_chain):
    mock_code_reader.read_file.return_value = "class A: pass"

    with patch('agent.generator.config'):
        generator = DocGenerator()
        result = generator.generate_mermaid("test.py")

        assert result == "Generated Documentation"
        mock_llm_chain.invoke.assert_called()

def test_api_ref_generation(mock_code_reader, mock_llm_chain):
    mock_code_reader.read_file.return_value = "def api(): pass"

    with patch('agent.generator.config'):
        generator = DocGenerator()
        result = generator.generate_api_ref("test.py")

        assert result == "Generated Documentation"
        mock_llm_chain.invoke.assert_called()

def test_empty_file(mock_code_reader, mock_llm_chain):
    mock_code_reader.read_file.return_value = ""
    with patch('agent.generator.config') as mock_config:
        mock_config.MODEL_NAME = "gpt-4"
        mock_config.OPENAI_API_KEY = "sk-test"
        generator = DocGenerator()
        result = generator.generate_doc("empty.py")
        assert result == ""
