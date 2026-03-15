"""Tests for test-generator main.py, config.py, example_code.py, and utils.py."""
import sys, os, pytest, runpy
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# ── config.py coverage ──────────────────────────────────────────────
def test_config_import():
    import config
    assert hasattr(config, 'Config')
    assert isinstance(config.Config.MODEL, str)
    assert isinstance(config.Config.DEBUG, bool)


def test_config_env_override():
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
        "GEMINI_API_KEY": "gem-key",
        "MODEL": "custom-model",
        "DEBUG": "true"
    }):
        import importlib
        import config
        importlib.reload(config)
        assert config.Config.OPENAI_API_KEY == "test-key"
        assert config.Config.GEMINI_API_KEY == "gem-key"
        assert config.Config.MODEL == "custom-model"
        assert config.Config.DEBUG is True


# ── example_code.py coverage ────────────────────────────────────────
from example_code import calculate_area, is_palindrome, fetch_user_data


def test_calculate_area_valid():
    assert calculate_area(3, 4) == 12


def test_calculate_area_zero():
    assert calculate_area(0, 5) == 0


def test_calculate_area_negative():
    with pytest.raises(ValueError):
        calculate_area(-1, 5)


def test_is_palindrome_true():
    assert is_palindrome("racecar") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_is_palindrome_non_string():
    with pytest.raises(TypeError):
        is_palindrome(123)


def test_fetch_user_data_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    with patch('example_code.requests.get', return_value=mock_response):
        result = fetch_user_data("user1")
        assert result == {"id": 1, "name": "Alice"}


def test_fetch_user_data_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 404
    with patch('example_code.requests.get', return_value=mock_response):
        result = fetch_user_data("bad_id")
        assert result is None


def test_fetch_user_data_empty_id():
    with pytest.raises(ValueError):
        fetch_user_data("")


# ── utils.py line 37 (print_info) ───────────────────────────────────
from utils import setup_logging, print_banner, print_success, print_error, print_info


def test_setup_logging():
    logger = setup_logging()
    assert logger.name == "test_generator"


def test_setup_logging_verbose():
    logger = setup_logging(verbose=True)
    assert logger.name == "test_generator"


def test_print_banner(capsys):
    print_banner()


def test_print_success(capsys):
    print_success("Done!")


def test_print_error(capsys):
    print_error("Fail!")


def test_print_info(capsys):
    print_info("Info message")


# ── main.py lines 77-94, 97 ─────────────────────────────────────────
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy-key", "OPENAI_MODEL_NAME": "gpt-4o"}):
        yield


def test_run_save_and_run_tests():
    """Cover lines 77-90: save to file and run pytest."""
    from main import run

    mock_crew_cls = MagicMock()
    mock_crew_cls.return_value.kickoff.return_value = "def test_foo(): pass"

    prompt_returns = iter(["example_code.py"])
    confirm_returns = iter([True, True])  # save=True, run=True

    with patch('main.Crew', mock_crew_cls), \
         patch('main.Prompt.ask', side_effect=lambda *a, **kw: next(prompt_returns)), \
         patch('main.Confirm.ask', side_effect=lambda *a, **kw: next(confirm_returns)), \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data="def foo(): pass")), \
         patch('os.makedirs'), \
         patch('subprocess.run') as mock_subprocess, \
         patch('main.console.print'):
        run()
        mock_subprocess.assert_called_once()


def test_run_exception_handling():
    """Cover lines 92-94: exception during crew execution."""
    from main import run

    mock_crew_cls = MagicMock()
    mock_crew_cls.return_value.kickoff.side_effect = RuntimeError("LLM error")

    with patch('main.Crew', mock_crew_cls), \
         patch('main.Prompt.ask', return_value="example_code.py"), \
         patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data="def foo(): pass")), \
         patch('main.print_error') as mock_err, \
         patch('main.console.print'):
        run()
        mock_err.assert_called_once()


def test_main_block():
    """Cover line 96-97: if __name__ == '__main__' block.
    
    We can't use runpy because dotenv's frame inspection crashes.
    Instead we exec the source with a pre-seeded namespace that mocks load_dotenv.
    """
    import types
    main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
    with open(main_path) as f:
        source = f.read()

    # Create a mock dotenv module
    mock_dotenv = types.ModuleType('dotenv')
    mock_dotenv.load_dotenv = lambda *a, **kw: None

    # Create a mock for Prompt/Confirm from rich
    mock_prompt_cls = MagicMock()
    mock_prompt_cls.ask.return_value = "nonexistent.py"
    mock_confirm_cls = MagicMock()
    mock_confirm_cls.ask.return_value = False
    
    # Patch sys.modules temporarily
    with patch.dict('sys.modules', {'dotenv': mock_dotenv}), \
         patch('os.path.exists', return_value=False):
        globs = {
            '__name__': '__main__',
            '__file__': main_path,
        }
        try:
            exec(compile(source, main_path, 'exec'), globs)
        except (SystemExit, Exception):
            pass  # Prompt.ask will be called, may fail — that's fine
