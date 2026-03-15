import os
import sys
import json
import runpy
from io import StringIO
from unittest.mock import patch, mock_open

# Ensure we have the parent directory in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import cmd_convert, cmd_languages, main
import config

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")

def test_cmd_convert(capsys):
    collection_data = {
        "item": [
            {"request": {"url": "http://example.com"}}
        ]
    }
    args = DummyArgs(collection="test.json", language="python")

    m = mock_open(read_data=json.dumps(collection_data))
    with patch("builtins.open", m):
        cmd_convert(args)

    captured = capsys.readouterr()
    assert "requests.get" in captured.out

def test_cmd_languages(capsys):
    args = DummyArgs()
    cmd_languages(args)
    captured = capsys.readouterr()
    assert "python" in captured.out
    assert "go" in captured.out

@patch("sys.argv", ["main.py", "convert", "collection.json", "--language", "python"])
def test_main_convert():
    with patch("main.cmd_convert") as mock_convert:
        main()
        mock_convert.assert_called_once()

@patch("sys.argv", ["main.py", "languages"])
def test_main_languages():
    with patch("main.cmd_languages") as mock_lang:
        main()
        mock_lang.assert_called_once()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "languages"]):
        with patch("main.cmd_languages"):
            runpy.run_path(script_path, run_name="__main__")
