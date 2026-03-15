import pytest
from unittest.mock import patch
import sys
import runpy

from main import cmd_generate, main
from config import Config

def test_config():
    assert Config is not None

def test_cmd_generate(capsys):
    class Args:
        language = "python"
        port = 8000
    cmd_generate(Args())
    captured = capsys.readouterr()
    assert "FROM python" in captured.out
    assert "EXPOSE 8000" in captured.out

def test_main():
    with patch("sys.argv", ["main.py", "generate", "node", "--port", "3000"]), \
         patch("main.cmd_generate") as mock_cmd:
        main()
        mock_cmd.assert_called_once()

def test_main_block():
    with patch("sys.argv", ["main.py", "generate", "go"]), \
         patch("main.cmd_generate") as mock_cmd:
        runpy.run_module("main", run_name="__main__")
