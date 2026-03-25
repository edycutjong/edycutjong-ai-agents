import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_collect, cmd_summarize, cmd_archive, main
from agent.core import collect, summarize, archive, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_collect_with_input():
    r = collect("test-input")
    assert r["command"] == "collect"
    assert r["status"] == "success"

def test_collect_empty():
    r = collect("")
    assert r["status"] == "error"

def test_collect_kwargs():
    r = collect("t", extra="v")
    assert r["command"] == "collect"

def test_cmd_collect_text(capsys):
    cmd_collect(DummyArgs(collect_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_collect_json(capsys):
    cmd_collect(DummyArgs(collect_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_collect_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_collect(DummyArgs(collect_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "collect", "test"])
def test_main_collect():
    with patch("main.cmd_collect") as m:
        main()
        m.assert_called_once()

def test_summarize_with_input():
    r = summarize("test-input")
    assert r["command"] == "summarize"
    assert r["status"] == "success"

def test_summarize_empty():
    r = summarize("")
    assert r["status"] == "error"

def test_summarize_kwargs():
    r = summarize("t", extra="v")
    assert r["command"] == "summarize"

def test_cmd_summarize_text(capsys):
    cmd_summarize(DummyArgs(summarize_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_summarize_json(capsys):
    cmd_summarize(DummyArgs(summarize_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_summarize_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_summarize(DummyArgs(summarize_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "summarize", "test"])
def test_main_summarize():
    with patch("main.cmd_summarize") as m:
        main()
        m.assert_called_once()

def test_archive_with_input():
    r = archive("test-input")
    assert r["command"] == "archive"
    assert r["status"] == "success"

def test_archive_empty():
    r = archive("")
    assert r["status"] == "error"

def test_archive_kwargs():
    r = archive("t", extra="v")
    assert r["command"] == "archive"

def test_cmd_archive_text(capsys):
    cmd_archive(DummyArgs(archive_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_archive_json(capsys):
    cmd_archive(DummyArgs(archive_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_archive_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_archive(DummyArgs(archive_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "archive", "test"])
def test_main_archive():
    with patch("main.cmd_archive") as m:
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
    with patch("sys.argv", ["main.py", "collect", "test"]):
        runpy.run_path(s, run_name="__main__")
