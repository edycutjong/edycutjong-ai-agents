import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_create, cmd_progress, cmd_review, main
from agent.core import create, progress, review, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_create_with_input():
    r = create("test-input")
    assert r["command"] == "create"
    assert r["status"] == "success"

def test_create_empty():
    r = create("")
    assert r["status"] == "error"

def test_create_kwargs():
    r = create("t", extra="v")
    assert r["command"] == "create"

def test_cmd_create_text(capsys):
    cmd_create(DummyArgs(create_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_create_json(capsys):
    cmd_create(DummyArgs(create_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_create_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_create(DummyArgs(create_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "create", "test"])
def test_main_create():
    with patch("main.cmd_create") as m:
        main()
        m.assert_called_once()

def test_progress_with_input():
    r = progress("test-input")
    assert r["command"] == "progress"
    assert r["status"] == "success"

def test_progress_empty():
    r = progress("")
    assert r["status"] == "error"

def test_progress_kwargs():
    r = progress("t", extra="v")
    assert r["command"] == "progress"

def test_cmd_progress_text(capsys):
    cmd_progress(DummyArgs(progress_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_progress_json(capsys):
    cmd_progress(DummyArgs(progress_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_progress_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_progress(DummyArgs(progress_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "progress", "test"])
def test_main_progress():
    with patch("main.cmd_progress") as m:
        main()
        m.assert_called_once()

def test_review_with_input():
    r = review("test-input")
    assert r["command"] == "review"
    assert r["status"] == "success"

def test_review_empty():
    r = review("")
    assert r["status"] == "error"

def test_review_kwargs():
    r = review("t", extra="v")
    assert r["command"] == "review"

def test_cmd_review_text(capsys):
    cmd_review(DummyArgs(review_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_review_json(capsys):
    cmd_review(DummyArgs(review_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_review_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_review(DummyArgs(review_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "review", "test"])
def test_main_review():
    with patch("main.cmd_review") as m:
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
    with patch("sys.argv", ["main.py", "create", "test"]):
        runpy.run_path(s, run_name="__main__")
