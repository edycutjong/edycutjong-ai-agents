import pytest
from unittest.mock import patch
import sys

@pytest.fixture(autouse=True)
def mock_all_inputs():
    """Globally mock built-in input, rich Prompt.ask and streamlit CLI main to prevent tests from hanging infinitely."""
    with patch("builtins.input", return_value="exit", create=True) as mock_input, \
         patch("rich.prompt.Prompt.ask", return_value="exit", create=True) as mock_rich_ask, \
         patch("streamlit.web.cli.main", return_value=0, create=True) as mock_st_main:
         
         # Also, some agents might try to hit real OpenAI / LLM APIs. We patch base classes if desired.
         # For now, fixing inputs should fix the majority of the hangs.
         yield mock_input, mock_rich_ask, mock_st_main
