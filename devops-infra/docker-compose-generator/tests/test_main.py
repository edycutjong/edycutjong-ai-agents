import pytest
from unittest.mock import patch
import sys
import runpy

from main import cmd_generate, cmd_list, main
from config import Config
from agent.generator import yaml_serialize

def test_config():
    assert Config is not None

def test_cmd_generate(capsys):
    class Args:
        services = ["postgres", "redis"]
    cmd_generate(Args())
    captured = capsys.readouterr()
    assert "version:" in captured.out
    assert "postgres:" in captured.out
    assert "redis:" in captured.out

def test_cmd_list(capsys):
    class Args:
        pass
    cmd_list(Args())
    captured = capsys.readouterr()
    assert "- postgres" in captured.out
    assert "- redis" in captured.out

def test_yaml_serialize_list_of_dicts():
    data = {
        "items": [
            {"name": "foo", "value": "bar"},
            {"name": "baz", "value": "qux", "extra": "info"}
        ]
    }
    result = yaml_serialize(data)
    expected = "\n".join([
        "items:",
        "  - name: foo",
        "    value: bar",
        "  - name: baz",
        "    value: qux",
        "    extra: info"
    ])
    assert result == expected

def test_main_generate():
    with patch("sys.argv", ["main.py", "generate", "postgres"]), \
         patch("main.cmd_generate") as mock_cmd:
        main()
        mock_cmd.assert_called_once()

def test_main_list():
    with patch("sys.argv", ["main.py", "list"]), \
         patch("main.cmd_list") as mock_cmd:
        main()
        mock_cmd.assert_called_once()

def test_main_block():
    with patch("sys.argv", ["main.py", "list"]), \
         patch("sys.stdout"):
        runpy.run_module("main", run_name="__main__")
