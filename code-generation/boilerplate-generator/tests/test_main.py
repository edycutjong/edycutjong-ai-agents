import os
import sys
import runpy
from io import StringIO
from unittest.mock import patch, MagicMock

# Ensure we have the parent directory in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import cmd_generate, cmd_list, main
import config

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")

def test_cmd_generate_markdown(capsys):
    args = DummyArgs(name="test_proj", template="python-cli", output=None)
    cmd_generate(args)
    captured = capsys.readouterr()
    assert "Generated: test_proj" in captured.out

def test_cmd_generate_output(capsys, tmp_path):
    out_dir = str(tmp_path / "out")
    args = DummyArgs(name="test_proj", template="python-cli", output=out_dir)
    cmd_generate(args)
    captured = capsys.readouterr()
    assert "Created" in captured.out
    assert os.path.exists(out_dir)

def test_cmd_list(capsys):
    args = DummyArgs()
    cmd_list(args)
    captured = capsys.readouterr()
    assert "python-cli" in captured.out

@patch("sys.argv", ["main.py", "generate", "proj", "--template", "python-cli"])
def test_main_generate():
    with patch("main.cmd_generate") as mock_gen:
        main()
        mock_gen.assert_called_once()

@patch("sys.argv", ["main.py", "list"])
def test_main_list():
    with patch("main.cmd_list") as mock_list:
        main()
        mock_list.assert_called_once()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "list"]):
        with patch("main.cmd_list"):
            runpy.run_path(script_path, run_name="__main__")
