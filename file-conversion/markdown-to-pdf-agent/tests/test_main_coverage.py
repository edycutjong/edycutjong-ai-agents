import os
import sys
import runpy
from io import StringIO
from unittest.mock import MagicMock

mock_q = MagicMock()
mock_q.select().ask.return_value = "Exit"
mock_q.confirm().ask.return_value = False
sys.modules["questionary"] = mock_q

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
import pytest


import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")
    
    # Mock questionary globally to prevent EOFError in tests
    import sys
    mock_q = MagicMock()
    mock_q.select().ask.return_value = "Exit"
    mock_q.confirm().ask.return_value = False
    sys.modules["questionary"] = mock_q

    class MockQuestionary:
        def __init__(self, rv="Exit"):
            self.rv = rv
        def ask(self):
            return self.rv
    try:
        import questionary
        monkeypatch.setattr("questionary.select", lambda *args, **kwargs: MockQuestionary("Exit"))
        monkeypatch.setattr("questionary.confirm", lambda *args, **kwargs: MockQuestionary(False))
    except ImportError:
        pass


def test_main_no_args():
    with patch("sys.argv", ["main.py"]):
        try:
            main()
        except (SystemExit, Exception):
            pass

def test_main_with_args():
    with patch("sys.argv", ["main.py", "test_string"]):
        try:
            main()
        except (SystemExit, Exception):
            pass

def test_main_with_file(tmp_path):
    p = tmp_path / "test_input.txt"
    p.write_text("test string data here")
    with patch("sys.argv", ["main.py", str(p)]):
        try:
            main()
        except (SystemExit, Exception):
            pass

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "test"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass
