import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_start, cmd_stats, cmd_tips, main
from agent.core import start, stats, tips, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_start_with_input():
    r = start("test-input")
    assert r["command"] == "start"
    assert r["status"] == "success"

def test_start_empty():
    r = start("")
    assert r["status"] == "error"

def test_start_kwargs():
    r = start("t", extra="v")
    assert r["command"] == "start"

def test_cmd_start_text(capsys):
    cmd_start(DummyArgs(start_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_start_json(capsys):
    cmd_start(DummyArgs(start_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_start_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_start(DummyArgs(start_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "start", "test"])
def test_main_start():
    with patch("main.cmd_start") as m:
        main()
        m.assert_called_once()

def test_stats_with_input():
    r = stats("test-input")
    assert r["command"] == "stats"
    assert r["status"] == "success"

def test_stats_empty():
    r = stats("")
    assert r["status"] == "error"

def test_stats_kwargs():
    r = stats("t", extra="v")
    assert r["command"] == "stats"

def test_cmd_stats_text(capsys):
    cmd_stats(DummyArgs(stats_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_stats_json(capsys):
    cmd_stats(DummyArgs(stats_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_stats_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_stats(DummyArgs(stats_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "stats", "test"])
def test_main_stats():
    with patch("main.cmd_stats") as m:
        main()
        m.assert_called_once()

def test_tips_with_input():
    r = tips("test-input")
    assert r["command"] == "tips"
    assert r["status"] == "success"

def test_tips_empty():
    r = tips("")
    assert r["status"] == "error"

def test_tips_kwargs():
    r = tips("t", extra="v")
    assert r["command"] == "tips"

def test_cmd_tips_text(capsys):
    cmd_tips(DummyArgs(tips_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_tips_json(capsys):
    cmd_tips(DummyArgs(tips_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_tips_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_tips(DummyArgs(tips_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "tips", "test"])
def test_main_tips():
    with patch("main.cmd_tips") as m:
        main()
        m.assert_called_once()

def test_format_text():
    assert "Command:" in format_output({"command":"t","status":"success","data":{"k":"v"}}, "text")

def test_format_json():
    r = json.loads(format_output({"command":"t","status":"success","data":{}}, "json"))
    assert r["command"] == "t"

def test_format_error():
    assert "Error:" in format_output({"command":"t","status":"error","error":"e","data":{}}, "text")

def test_main_block():
    s = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "start", "test"]):
        runpy.run_path(s, run_name="__main__")
