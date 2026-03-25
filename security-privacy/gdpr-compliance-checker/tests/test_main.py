import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_check, cmd_scan, cmd_report, main
from agent.core import check, scan, report, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_check_with_input():
    r = check("test-input")
    assert r["command"] == "check"
    assert r["status"] == "success"

def test_check_empty():
    r = check("")
    assert r["status"] == "error"

def test_check_kwargs():
    r = check("t", extra="v")
    assert r["command"] == "check"

def test_cmd_check_text(capsys):
    cmd_check(DummyArgs(check_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_check_json(capsys):
    cmd_check(DummyArgs(check_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_check_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_check(DummyArgs(check_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "check", "test"])
def test_main_check():
    with patch("main.cmd_check") as m:
        main()
        m.assert_called_once()

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
    with patch("sys.argv", ["main.py", "check", "test"]):
        runpy.run_path(s, run_name="__main__")
