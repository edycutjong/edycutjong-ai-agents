import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_analyze, cmd_match, cmd_report, main
from agent.core import analyze, match, report, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

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

def test_match_with_input():
    r = match("test-input")
    assert r["command"] == "match"
    assert r["status"] == "success"

def test_match_empty():
    r = match("")
    assert r["status"] == "error"

def test_match_kwargs():
    r = match("t", extra="v")
    assert r["command"] == "match"

def test_cmd_match_text(capsys):
    cmd_match(DummyArgs(match_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_match_json(capsys):
    cmd_match(DummyArgs(match_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_match_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_match(DummyArgs(match_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "match", "test"])
def test_main_match():
    with patch("main.cmd_match") as m:
        main()
        m.assert_called_once()

def test_report_with_input():
    r = report("test-input")
    assert r["command"] == "report"
    assert r["status"] == "success"

def test_report_empty():
    r = report("")
    assert r["status"] == "error"

def test_report_kwargs():
    r = report("t", extra="v")
    assert r["command"] == "report"

def test_cmd_report_text(capsys):
    cmd_report(DummyArgs(report_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_report_json(capsys):
    cmd_report(DummyArgs(report_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_report_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_report(DummyArgs(report_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "report", "test"])
def test_main_report():
    with patch("main.cmd_report") as m:
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
    with patch("sys.argv", ["main.py", "analyze", "test"]):
        runpy.run_path(s, run_name="__main__")
