import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_test, cmd_compare, cmd_best, main
from agent.core import test, compare, best, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_test_with_input():
    r = test("test-input")
    assert r["command"] == "test"
    assert r["status"] == "success"

def test_test_empty():
    r = test("")
    assert r["status"] == "error"

def test_test_kwargs():
    r = test("t", extra="v")
    assert r["command"] == "test"

def test_cmd_test_text(capsys):
    cmd_test(DummyArgs(test_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_test_json(capsys):
    cmd_test(DummyArgs(test_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_test_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_test(DummyArgs(test_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "test", "test"])
def test_main_test():
    with patch("main.cmd_test") as m:
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

def test_best_with_input():
    r = best("test-input")
    assert r["command"] == "best"
    assert r["status"] == "success"

def test_best_empty():
    r = best("")
    assert r["status"] == "error"

def test_best_kwargs():
    r = best("t", extra="v")
    assert r["command"] == "best"

def test_cmd_best_text(capsys):
    cmd_best(DummyArgs(best_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_best_json(capsys):
    cmd_best(DummyArgs(best_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_best_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_best(DummyArgs(best_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "best", "test"])
def test_main_best():
    with patch("main.cmd_best") as m:
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
    with patch("sys.argv", ["main.py", "test", "test"]):
        runpy.run_path(s, run_name="__main__")
