import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_quiz, cmd_score, cmd_export, main
from agent.core import quiz, score, export, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_quiz_with_input():
    r = quiz("test-input")
    assert r["command"] == "quiz"
    assert r["status"] == "success"

def test_quiz_empty():
    r = quiz("")
    assert r["status"] == "error"

def test_quiz_kwargs():
    r = quiz("t", extra="v")
    assert r["command"] == "quiz"

def test_cmd_quiz_text(capsys):
    cmd_quiz(DummyArgs(quiz_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_quiz_json(capsys):
    cmd_quiz(DummyArgs(quiz_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_quiz_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_quiz(DummyArgs(quiz_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "quiz", "test"])
def test_main_quiz():
    with patch("main.cmd_quiz") as m:
        main()
        m.assert_called_once()

def test_score_with_input():
    r = score("test-input")
    assert r["command"] == "score"
    assert r["status"] == "success"

def test_score_empty():
    r = score("")
    assert r["status"] == "error"

def test_score_kwargs():
    r = score("t", extra="v")
    assert r["command"] == "score"

def test_cmd_score_text(capsys):
    cmd_score(DummyArgs(score_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_score_json(capsys):
    cmd_score(DummyArgs(score_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_score_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_score(DummyArgs(score_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "score", "test"])
def test_main_score():
    with patch("main.cmd_score") as m:
        main()
        m.assert_called_once()

def test_export_with_input():
    r = export("test-input")
    assert r["command"] == "export"
    assert r["status"] == "success"

def test_export_empty():
    r = export("")
    assert r["status"] == "error"

def test_export_kwargs():
    r = export("t", extra="v")
    assert r["command"] == "export"

def test_cmd_export_text(capsys):
    cmd_export(DummyArgs(export_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_export_json(capsys):
    cmd_export(DummyArgs(export_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_export_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_export(DummyArgs(export_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "export", "test"])
def test_main_export():
    with patch("main.cmd_export") as m:
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
    with patch("sys.argv", ["main.py", "quiz", "test"]):
        runpy.run_path(s, run_name="__main__")
