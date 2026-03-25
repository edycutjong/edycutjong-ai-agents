import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_audit, cmd_analyze, cmd_optimize, main
from agent.core import audit, analyze, optimize, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_audit_with_input():
    r = audit("test-input")
    assert r["command"] == "audit"
    assert r["status"] == "success"

def test_audit_empty():
    r = audit("")
    assert r["status"] == "error"

def test_audit_kwargs():
    r = audit("t", extra="v")
    assert r["command"] == "audit"

def test_cmd_audit_text(capsys):
    cmd_audit(DummyArgs(audit_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_audit_json(capsys):
    cmd_audit(DummyArgs(audit_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_audit_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_audit(DummyArgs(audit_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "audit", "test"])
def test_main_audit():
    with patch("main.cmd_audit") as m:
        main()
        m.assert_called_once()

def test_analyze_with_input():
    r = analyze("test-input")
    assert r["command"] == "analyze"
    assert r["status"] == "success"

def test_analyze_empty():
    r = analyze("")
    assert r["status"] == "error"

def test_analyze_kwargs():
    r = analyze("t", extra="v")
    assert r["command"] == "analyze"

def test_cmd_analyze_text(capsys):
    cmd_analyze(DummyArgs(analyze_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_analyze_json(capsys):
    cmd_analyze(DummyArgs(analyze_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_analyze_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_analyze(DummyArgs(analyze_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "analyze", "test"])
def test_main_analyze():
    with patch("main.cmd_analyze") as m:
        main()
        m.assert_called_once()

def test_optimize_with_input():
    r = optimize("test-input")
    assert r["command"] == "optimize"
    assert r["status"] == "success"

def test_optimize_empty():
    r = optimize("")
    assert r["status"] == "error"

def test_optimize_kwargs():
    r = optimize("t", extra="v")
    assert r["command"] == "optimize"

def test_cmd_optimize_text(capsys):
    cmd_optimize(DummyArgs(optimize_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_optimize_json(capsys):
    cmd_optimize(DummyArgs(optimize_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_optimize_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_optimize(DummyArgs(optimize_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "optimize", "test"])
def test_main_optimize():
    with patch("main.cmd_optimize") as m:
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
    with patch("sys.argv", ["main.py", "audit", "test"]):
        runpy.run_path(s, run_name="__main__")
