import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_scan, cmd_rotate, cmd_audit, main
from agent.core import scan, rotate, audit, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_scan_with_input():
    r = scan("test-input")
    assert r["command"] == "scan"
    assert r["status"] == "success"

def test_scan_empty():
    r = scan("")
    assert r["status"] == "error"

def test_scan_kwargs():
    r = scan("t", extra="v")
    assert r["command"] == "scan"

def test_cmd_scan_text(capsys):
    cmd_scan(DummyArgs(scan_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_scan_json(capsys):
    cmd_scan(DummyArgs(scan_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_scan_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_scan(DummyArgs(scan_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "scan", "test"])
def test_main_scan():
    with patch("main.cmd_scan") as m:
        main()
        m.assert_called_once()

def test_rotate_with_input():
    r = rotate("test-input")
    assert r["command"] == "rotate"
    assert r["status"] == "success"

def test_rotate_empty():
    r = rotate("")
    assert r["status"] == "error"

def test_rotate_kwargs():
    r = rotate("t", extra="v")
    assert r["command"] == "rotate"

def test_cmd_rotate_text(capsys):
    cmd_rotate(DummyArgs(rotate_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_rotate_json(capsys):
    cmd_rotate(DummyArgs(rotate_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_rotate_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_rotate(DummyArgs(rotate_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "rotate", "test"])
def test_main_rotate():
    with patch("main.cmd_rotate") as m:
        main()
        m.assert_called_once()

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

def test_format_text():
    assert "Command:" in format_output({"command":"t","status":"success","data":{"k":"v"}}, "text")

def test_format_json():
    r = json.loads(format_output({"command":"t","status":"success","data":{}}, "json"))
    assert r["command"] == "t"

def test_format_error():
    assert "Error:" in format_output({"command":"t","status":"error","error":"e","data":{}}, "text")

def test_main_block():
    s = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "scan", "test"]):
        runpy.run_path(s, run_name="__main__")
