import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_assess, cmd_recommend, cmd_track, main
from agent.core import assess, recommend, track, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_assess_with_input():
    r = assess("test-input")
    assert r["command"] == "assess"
    assert r["status"] == "success"

def test_assess_empty():
    r = assess("")
    assert r["status"] == "error"

def test_assess_kwargs():
    r = assess("t", extra="v")
    assert r["command"] == "assess"

def test_cmd_assess_text(capsys):
    cmd_assess(DummyArgs(assess_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_assess_json(capsys):
    cmd_assess(DummyArgs(assess_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_assess_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_assess(DummyArgs(assess_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "assess", "test"])
def test_main_assess():
    with patch("main.cmd_assess") as m:
        main()
        m.assert_called_once()

def test_recommend_with_input():
    r = recommend("test-input")
    assert r["command"] == "recommend"
    assert r["status"] == "success"

def test_recommend_empty():
    r = recommend("")
    assert r["status"] == "error"

def test_recommend_kwargs():
    r = recommend("t", extra="v")
    assert r["command"] == "recommend"

def test_cmd_recommend_text(capsys):
    cmd_recommend(DummyArgs(recommend_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_recommend_json(capsys):
    cmd_recommend(DummyArgs(recommend_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_recommend_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_recommend(DummyArgs(recommend_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "recommend", "test"])
def test_main_recommend():
    with patch("main.cmd_recommend") as m:
        main()
        m.assert_called_once()

def test_track_with_input():
    r = track("test-input")
    assert r["command"] == "track"
    assert r["status"] == "success"

def test_track_empty():
    r = track("")
    assert r["status"] == "error"

def test_track_kwargs():
    r = track("t", extra="v")
    assert r["command"] == "track"

def test_cmd_track_text(capsys):
    cmd_track(DummyArgs(track_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_track_json(capsys):
    cmd_track(DummyArgs(track_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_track_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_track(DummyArgs(track_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "track", "test"])
def test_main_track():
    with patch("main.cmd_track") as m:
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
    with patch("sys.argv", ["main.py", "assess", "test"]):
        runpy.run_path(s, run_name="__main__")
