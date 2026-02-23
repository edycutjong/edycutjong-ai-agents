import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to path to allow importing 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.translator import Translator

@patch("tools.translator.ChatOpenAI")
@patch("tools.translator.ChatPromptTemplate")
@patch("tools.translator.JsonOutputParser")
def test_translate_keys(mock_parser_cls, mock_prompt_cls, mock_openai_cls):
    # Setup mocks
    mock_llm = MagicMock()
    mock_openai_cls.return_value = mock_llm

    mock_prompt = MagicMock()
    mock_prompt_cls.from_template.return_value = mock_prompt

    mock_parser = MagicMock()
    mock_parser_cls.return_value = mock_parser

    # Mock the chain: prompt | llm | parser
    # The `|` operator returns a new Runnable.
    # We need to ensure that `mock_prompt | mock_llm | mock_parser` results in a mock chain.

    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"hello": "Hola"}

    # We can configure `__or__` (the bitwise OR operator used for piping in LangChain)
    # prompt | llm -> intermediate
    # intermediate | parser -> chain

    intermediate_mock = MagicMock()
    mock_prompt.__or__.return_value = intermediate_mock
    intermediate_mock.__or__.return_value = mock_chain

    # Create Translator
    translator = Translator(api_key="sk-test")

    # Call translate_keys
    result = translator.translate_keys(["hello"], "es")

    # Verify
    assert result == {"hello": "Hola"}
    mock_chain.invoke.assert_called_once()

    # Verify arguments passed to invoke
    args, _ = mock_chain.invoke.call_args
    assert args[0]["target_lang"] == "es"
    # assert args[0]["keys"] contains 'hello'

def test_translate_keys_empty():
    translator = Translator(api_key="sk-test")
    result = translator.translate_keys([], "es")
    assert result == {}
