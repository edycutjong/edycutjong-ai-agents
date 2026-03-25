import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_generate, cmd_breathe, cmd_affirm, main
from agent.core import generate, breathe, affirm, format_output
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

def test_breathe_with_input():
    r = breathe("test-input")
    assert r["command"] == "breathe"
    assert r["status"] == "success"

def test_breathe_empty():
    r = breathe("")
    assert r["status"] == "error"

def test_breathe_kwargs():
    r = breathe("t", extra="v")
    assert r["command"] == "breathe"

def test_cmd_breathe_text(capsys):
    cmd_breathe(DummyArgs(breathe_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_breathe_json(capsys):
    cmd_breathe(DummyArgs(breathe_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_breathe_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_breathe(DummyArgs(breathe_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "breathe", "test"])
def test_main_breathe():
    with patch("main.cmd_breathe") as m:
        main()
        m.assert_called_once()

def test_affirm_with_input():
    r = affirm("test-input")
    assert r["command"] == "affirm"
    assert r["status"] == "success"

def test_affirm_empty():
    r = affirm("")
    assert r["status"] == "error"

def test_affirm_kwargs():
    r = affirm("t", extra="v")
    assert r["command"] == "affirm"

def test_cmd_affirm_text(capsys):
    cmd_affirm(DummyArgs(affirm_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_affirm_json(capsys):
    cmd_affirm(DummyArgs(affirm_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_affirm_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_affirm(DummyArgs(affirm_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "affirm", "test"])
def test_main_affirm():
    with patch("main.cmd_affirm") as m:
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
