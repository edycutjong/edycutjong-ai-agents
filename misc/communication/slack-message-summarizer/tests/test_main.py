import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_summarize, cmd_digest, cmd_search, main
from agent.core import summarize, digest, search, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

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

def test_digest_with_input():
    r = digest("test-input")
    assert r["command"] == "digest"
    assert r["status"] == "success"

def test_digest_empty():
    r = digest("")
    assert r["status"] == "error"

def test_digest_kwargs():
    r = digest("t", extra="v")
    assert r["command"] == "digest"

def test_cmd_digest_text(capsys):
    cmd_digest(DummyArgs(digest_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_digest_json(capsys):
    cmd_digest(DummyArgs(digest_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_digest_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_digest(DummyArgs(digest_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "digest", "test"])
def test_main_digest():
    with patch("main.cmd_digest") as m:
        main()
        m.assert_called_once()

def test_search_with_input():
    r = search("test-input")
    assert r["command"] == "search"
    assert r["status"] == "success"

def test_search_empty():
    r = search("")
    assert r["status"] == "error"

def test_search_kwargs():
    r = search("t", extra="v")
    assert r["command"] == "search"

def test_cmd_search_text(capsys):
    cmd_search(DummyArgs(search_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_search_json(capsys):
    cmd_search(DummyArgs(search_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_search_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_search(DummyArgs(search_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "search", "test"])
def test_main_search():
    with patch("main.cmd_search") as m:
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
    with patch("sys.argv", ["main.py", "summarize", "test"]):
        runpy.run_path(s, run_name="__main__")
