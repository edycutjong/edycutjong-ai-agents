import os
import sys
import runpy
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import cmd_generate, main
import config
from agent.generator import ProjectInfo

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")

def test_cmd_generate_with_dir(capsys):
    args = DummyArgs(dir="test_dir", name=None, template=None)
    with patch("main.detect_project") as mock_detect:
        mock_detect.return_value = ProjectInfo(name="test_proj")
        cmd_generate(args)
    captured = capsys.readouterr()
    assert "# test_proj" in captured.out

def test_cmd_generate_with_template(capsys):
    args = DummyArgs(dir=None, name="test_api", template="api")
    cmd_generate(args)
    captured = capsys.readouterr()
    assert "# test_api" in captured.out
    assert "REST API" in captured.out

@patch("sys.argv", ["main.py", "generate", "--template", "minimal"])
def test_main_func():
    with patch("main.cmd_generate") as mock_gen:
        main()
        mock_gen.assert_called_once()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "generate", "--template", "api"]):
        with patch("main.cmd_generate"):
            runpy.run_path(script_path, run_name="__main__")
