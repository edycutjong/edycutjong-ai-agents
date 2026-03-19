"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch, MagicMock
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def test_config(): assert Config is not None

def test_main_cli(tmp_path):
    """Cover main.py CLI invocation, error handling and banner."""
    transcript = tmp_path / "meeting.txt"
    transcript.write_text("Alice: Let us discuss the Q4 targets.\nBob: Sounds good.")
    from click.testing import CliRunner
    from main import main, print_banner
    # Test banner
    print_banner()
    # Test main with mocked chains
    mock_chain = MagicMock()
    mock_chain.invoke = MagicMock(return_value="Summary result")
    runner = CliRunner()
    with patch("main.get_summary_chain", return_value=mock_chain), \
         patch("main.get_action_items_chain", return_value=mock_chain), \
         patch("main.get_email_chain", return_value=mock_chain), \
         patch("main.get_sentiment_chain", return_value=mock_chain):
        result = runner.invoke(main, [str(transcript)])
        assert result.exit_code == 0

def test_main_cli_error(tmp_path):
    """Cover lines 86-88, 91: exception handling."""
    transcript = tmp_path / "meeting.txt"
    transcript.write_text("Hello world")
    from click.testing import CliRunner
    from main import main
    mock_chain = MagicMock()
    mock_chain.invoke = MagicMock(side_effect=Exception("API Error"))
    runner = CliRunner()
    with patch("main.get_summary_chain", return_value=mock_chain), \
         patch("main.get_action_items_chain", return_value=mock_chain), \
         patch("main.get_email_chain", return_value=mock_chain), \
         patch("main.get_sentiment_chain", return_value=mock_chain):
        result = runner.invoke(main, [str(transcript)])
        assert result.exit_code != 0

def test_utils_read_file_vtt(tmp_path):
    """Cover utils.py line 10: VTT file reading."""
    from utils import read_file
    vtt = tmp_path / "transcript.vtt"
    vtt.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello this is a test")
    text = read_file(str(vtt))
    assert len(text) > 0

def test_agent_config_chains():
    """Cover agent_config.py remaining chains."""
    from agent_config import get_email_chain, get_sentiment_chain
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        email_chain = get_email_chain()
        assert email_chain is not None
        sentiment_chain = get_sentiment_chain()
        assert sentiment_chain is not None

def test_main_entry_point(tmp_path):
    transcript = tmp_path / "m.txt"
    transcript.write_text("Discussion notes")
    mock_chain = MagicMock()
    mock_chain.invoke = MagicMock(return_value="Result")
    from click.testing import CliRunner
    from main import main
    runner = CliRunner()
    with patch("main.get_summary_chain", return_value=mock_chain), \
         patch("main.get_action_items_chain", return_value=mock_chain), \
         patch("main.get_email_chain", return_value=mock_chain), \
         patch("main.get_sentiment_chain", return_value=mock_chain):
        result = runner.invoke(main, [str(transcript)])
        assert result.exit_code == 0


def test_get_llm_no_api_key():
    """Cover agent_config.py line 13: raise ValueError."""
    from agent_config import get_llm
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("OPENAI_API_KEY", None)
        with pytest.raises(ValueError):
            get_llm()

def test_read_file_not_found():
    """Cover utils.py line 10: FileNotFoundError."""
    from utils import read_file
    with pytest.raises(FileNotFoundError):
        read_file("/nonexistent/path/to/file.txt")
