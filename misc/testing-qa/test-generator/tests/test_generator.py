import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import run

@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key", "OPENAI_MODEL_NAME": "gpt-4o"}):
        yield

@pytest.fixture
def mock_crew():
    with patch('main.Crew') as MockCrew:
        instance = MockCrew.return_value
        instance.kickoff.return_value = "def test_example(): pass"
        yield instance

@pytest.fixture
def mock_prompt():
    with patch('main.Prompt.ask') as MockAsk:
        MockAsk.return_value = "example_code.py"
        yield MockAsk

@pytest.fixture
def mock_confirm():
    with patch('main.Confirm.ask') as MockConfirm:
        MockConfirm.return_value = False
        yield MockConfirm

@pytest.fixture
def mock_console_print():
    with patch('main.console.print') as MockPrint:
        yield MockPrint

@pytest.fixture
def mock_utils_print_error():
    with patch('main.print_error') as MockPrintError:
        yield MockPrintError

def test_run_success(mock_crew, mock_prompt, mock_confirm, mock_console_print):
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', new_callable=MagicMock) as mock_open:

        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "def foo(): pass"
        mock_open.return_value = mock_file

        run()

        assert mock_crew.kickoff.called
        assert mock_console_print.called

def test_file_not_found(mock_prompt, mock_utils_print_error):
    with patch('os.path.exists', return_value=False):
        run()
        assert mock_utils_print_error.called
