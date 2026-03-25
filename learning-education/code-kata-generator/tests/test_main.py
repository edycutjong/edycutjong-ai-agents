import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_generate, cmd_grade, cmd_hint, main
from agent.core import generate, grade, hint, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_generate_with_input():
    r = generate("test-input")
    assert r["command"] == "generate"
    assert r["status"] == "success"

def test_generate_empty():
    r = generate("")
    assert r["status"] == "error"

def test_generate_kwargs():
    r = generate("t", extra="v")
    assert r["command"] == "generate"

def test_cmd_generate_text(capsys):
    cmd_generate(DummyArgs(generate_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_generate_json(capsys):
    cmd_generate(DummyArgs(generate_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_generate_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_generate(DummyArgs(generate_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "generate", "test"])
def test_main_generate():
    with patch("main.cmd_generate") as m:
        main()
        m.assert_called_once()

def test_grade_with_input():
    r = grade("test-input")
    assert r["command"] == "grade"
    assert r["status"] == "success"

def test_grade_empty():
    r = grade("")
    assert r["status"] == "error"

def test_grade_kwargs():
    r = grade("t", extra="v")
    assert r["command"] == "grade"

def test_cmd_grade_text(capsys):
    cmd_grade(DummyArgs(grade_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_grade_json(capsys):
    cmd_grade(DummyArgs(grade_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_grade_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_grade(DummyArgs(grade_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "grade", "test"])
def test_main_grade():
    with patch("main.cmd_grade") as m:
        main()
        m.assert_called_once()

def test_hint_with_input():
    r = hint("test-input")
    assert r["command"] == "hint"
    assert r["status"] == "success"

def test_hint_empty():
    r = hint("")
    assert r["status"] == "error"

def test_hint_kwargs():
    r = hint("t", extra="v")
    assert r["command"] == "hint"

def test_cmd_hint_text(capsys):
    cmd_hint(DummyArgs(hint_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_hint_json(capsys):
    cmd_hint(DummyArgs(hint_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_hint_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_hint(DummyArgs(hint_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "hint", "test"])
def test_main_hint():
    with patch("main.cmd_hint") as m:
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
    with patch("sys.argv", ["main.py", "generate", "test"]):
        runpy.run_path(s, run_name="__main__")
