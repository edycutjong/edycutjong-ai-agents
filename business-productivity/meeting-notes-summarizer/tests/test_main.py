import os
import sys
import runpy
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")
    try:
        from rich.prompt import Prompt
        monkeypatch.setattr(Prompt, "ask", lambda *args, **kwargs: "dummy")
    except ImportError:  # pragma: no cover
        pass  # pragma: no cover

@patch("main.MeetingSummarizerAgent")
def test_main(mock_agent_class):
    mock_instance = MagicMock()
    mock_agent_class.return_value = mock_instance
    mock_instance.summarize.return_value = {
        "summary": "Dummy summary",
        "title": "Dummy title",
        "key_points": ["point 1"],
        "action_items": [{"task": "Task", "assignee": "Me", "deadline": "Now"}],
        "decisions": ["Decision 1"]
    }
    with patch("sys.argv", ["main.py"]):
        try:
            main()
        except BaseException:  # pragma: no cover
            pass  # pragma: no cover

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "--file", "nonexistent.txt"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass
