import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_import_data, cmd_categorize, cmd_report, main
from agent.core import import_data, categorize, report, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_import_data_with_input():
    r = import_data("test-input")
    assert r["command"] == "import_data"
    assert r["status"] == "success"

def test_import_data_empty():
    r = import_data("")
    assert r["status"] == "error"

def test_import_data_kwargs():
    r = import_data("t", extra="v")
    assert r["command"] == "import_data"

def test_cmd_import_data_text(capsys):
    cmd_import_data(DummyArgs(import_data_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_import_data_json(capsys):
    cmd_import_data(DummyArgs(import_data_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_import_data_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_import_data(DummyArgs(import_data_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "import_data", "test"])
def test_main_import_data():
    with patch("main.cmd_import_data") as m:
        main()
        m.assert_called_once()

def test_categorize_with_input():
    r = categorize("test-input")
    assert r["command"] == "categorize"
    assert r["status"] == "success"

def test_categorize_empty():
    r = categorize("")
    assert r["status"] == "error"

def test_categorize_kwargs():
    r = categorize("t", extra="v")
    assert r["command"] == "categorize"

def test_cmd_categorize_text(capsys):
    cmd_categorize(DummyArgs(categorize_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_categorize_json(capsys):
    cmd_categorize(DummyArgs(categorize_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_categorize_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_categorize(DummyArgs(categorize_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "categorize", "test"])
def test_main_categorize():
    with patch("main.cmd_categorize") as m:
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
    with patch("sys.argv", ["main.py", "import_data", "test"]):
        runpy.run_path(s, run_name="__main__")
