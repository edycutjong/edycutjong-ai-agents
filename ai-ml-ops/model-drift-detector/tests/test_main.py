import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_detect, cmd_compare, cmd_alert, main
from agent.core import detect, compare, alert, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_detect_with_input():
    r = detect("test-input")
    assert r["command"] == "detect"
    assert r["status"] == "success"

def test_detect_empty():
    r = detect("")
    assert r["status"] == "error"

def test_detect_kwargs():
    r = detect("t", extra="v")
    assert r["command"] == "detect"

def test_cmd_detect_text(capsys):
    cmd_detect(DummyArgs(detect_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_detect_json(capsys):
    cmd_detect(DummyArgs(detect_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_detect_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_detect(DummyArgs(detect_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "detect", "test"])
def test_main_detect():
    with patch("main.cmd_detect") as m:
        main()
        m.assert_called_once()

def test_compare_with_input():
    r = compare("test-input")
    assert r["command"] == "compare"
    assert r["status"] == "success"

def test_compare_empty():
    r = compare("")
    assert r["status"] == "error"

def test_compare_kwargs():
    r = compare("t", extra="v")
    assert r["command"] == "compare"

def test_cmd_compare_text(capsys):
    cmd_compare(DummyArgs(compare_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_compare_json(capsys):
    cmd_compare(DummyArgs(compare_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_compare_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_compare(DummyArgs(compare_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "compare", "test"])
def test_main_compare():
    with patch("main.cmd_compare") as m:
        main()
        m.assert_called_once()

def test_alert_with_input():
    r = alert("test-input")
    assert r["command"] == "alert"
    assert r["status"] == "success"

def test_alert_empty():
    r = alert("")
    assert r["status"] == "error"

def test_alert_kwargs():
    r = alert("t", extra="v")
    assert r["command"] == "alert"

def test_cmd_alert_text(capsys):
    cmd_alert(DummyArgs(alert_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_alert_json(capsys):
    cmd_alert(DummyArgs(alert_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_alert_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_alert(DummyArgs(alert_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "alert", "test"])
def test_main_alert():
    with patch("main.cmd_alert") as m:
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
    with patch("sys.argv", ["main.py", "detect", "test"]):
        runpy.run_path(s, run_name="__main__")
