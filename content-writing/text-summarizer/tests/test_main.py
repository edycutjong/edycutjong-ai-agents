import os
import sys
import runpy
from io import StringIO
from unittest.mock import patch, mock_open

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import cmd_summarize, main
import config

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")

def test_cmd_summarize_stdin(capsys):
    args = DummyArgs(file="-", ratio=0.5)
    with patch("sys.stdin", StringIO("This is a test. It is a good test.")):
        cmd_summarize(args)
    captured = capsys.readouterr()
    assert "Original" in captured.out

def test_cmd_summarize_file(capsys):
    args = DummyArgs(file="test.txt", ratio=0.5)
    m = mock_open(read_data="This is a test. It is a good test.")
    with patch("builtins.open", m):
        cmd_summarize(args)
    captured = capsys.readouterr()
    assert "Original" in captured.out

@patch("sys.argv", ["main.py", "summarize", "-", "--ratio", "0.5"])
def test_main():
    with patch("main.cmd_summarize") as mock_sum:
        main()
        mock_sum.assert_called_once()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "summarize", "-"]):
        with patch("sys.stdin", StringIO("test")):
            runpy.run_path(script_path, run_name="__main__")
