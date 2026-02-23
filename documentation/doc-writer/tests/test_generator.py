import os
import sys
from unittest.mock import MagicMock, patch

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from doc_writer.generator import DocGenerator

@patch('doc_writer.generator.config')
@patch('doc_writer.generator.ChatOpenAI')
def test_generate_docstring(MockChatOpenAI, MockConfig):
    # Setup mock config
    MockConfig.OPENAI_API_KEY = "test-key"
    MockConfig.MODEL_NAME = "gpt-4o"

    # Initialize generator
    generator = DocGenerator()

    # Mock the chain
    generator.chain = MagicMock()
    generator.chain.invoke.return_value = '"""Google style docstring."""'

    snippet = "def foo(): pass"
    result = generator.generate_docstring(snippet)

    # Assertions
    # Note: The generator now strips triple quotes if present, but since our mock returns them,
    # and the generator strips them, the result should NOT have them if they match correctly.
    # Wait, the prompt says "Output ONLY the docstring content, without the triple quotes".
    # But if LLM outputs quotes, we strip them.
    # If mock returns '"""Google style docstring."""', generator should strip them.

    assert result == 'Google style docstring.'
    generator.chain.invoke.assert_called_once_with({"code_snippet": snippet})

@patch('doc_writer.generator.config')
@patch('doc_writer.generator.ChatOpenAI')
def test_generate_docstring_strips_quotes(MockChatOpenAI, MockConfig):
    MockConfig.OPENAI_API_KEY = "test-key"
    generator = DocGenerator()
    generator.chain = MagicMock()

    # Mock return WITH quotes
    generator.chain.invoke.return_value = '"""One line docstring."""'
    result = generator.generate_docstring("def foo(): pass")
    assert result == 'One line docstring.'

    # Mock return WITHOUT quotes (ideal case)
    generator.chain.invoke.return_value = 'Just a docstring.'
    result = generator.generate_docstring("def bar(): pass")
    assert result == 'Just a docstring.'

@patch('doc_writer.generator.config')
@patch('doc_writer.generator.ChatOpenAI')
def test_generate_docstring_error(MockChatOpenAI, MockConfig):
    MockConfig.OPENAI_API_KEY = "test-key"

    generator = DocGenerator()
    generator.chain = MagicMock()
    generator.chain.invoke.side_effect = Exception("API Error")

    snippet = "def foo(): pass"
    result = generator.generate_docstring(snippet)

    assert result == ""
