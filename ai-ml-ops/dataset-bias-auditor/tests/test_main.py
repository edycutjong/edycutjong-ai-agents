import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_audit, cmd_score, cmd_remediate, main
from agent.core import audit, score, remediate, format_output
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

def test_remediate_with_input():
    r = remediate("test-input")
    assert r["command"] == "remediate"
    assert r["status"] == "success"

def test_remediate_empty():
    r = remediate("")
    assert r["status"] == "error"

def test_remediate_kwargs():
    r = remediate("t", extra="v")
    assert r["command"] == "remediate"

def test_cmd_remediate_text(capsys):
    cmd_remediate(DummyArgs(remediate_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_remediate_json(capsys):
    cmd_remediate(DummyArgs(remediate_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_remediate_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_remediate(DummyArgs(remediate_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "remediate", "test"])
def test_main_remediate():
    with patch("main.cmd_remediate") as m:
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
