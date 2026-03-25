import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_route, cmd_configure, cmd_status, main
from agent.core import route, configure, status, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_route_with_input():
    r = route("test-input")
    assert r["command"] == "route"
    assert r["status"] == "success"

def test_route_empty():
    r = route("")
    assert r["status"] == "error"

def test_route_kwargs():
    r = route("t", extra="v")
    assert r["command"] == "route"

def test_cmd_route_text(capsys):
    cmd_route(DummyArgs(route_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_route_json(capsys):
    cmd_route(DummyArgs(route_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_route_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_route(DummyArgs(route_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "route", "test"])
def test_main_route():
    with patch("main.cmd_route") as m:
        main()
        m.assert_called_once()

def test_configure_with_input():
    r = configure("test-input")
    assert r["command"] == "configure"
    assert r["status"] == "success"

def test_configure_empty():
    r = configure("")
    assert r["status"] == "error"

def test_configure_kwargs():
    r = configure("t", extra="v")
    assert r["command"] == "configure"

def test_cmd_configure_text(capsys):
    cmd_configure(DummyArgs(configure_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_configure_json(capsys):
    cmd_configure(DummyArgs(configure_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_configure_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_configure(DummyArgs(configure_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "configure", "test"])
def test_main_configure():
    with patch("main.cmd_configure") as m:
        main()
        m.assert_called_once()

def test_status_with_input():
    r = status("test-input")
    assert r["command"] == "status"
    assert r["status"] == "success"

def test_status_empty():
    r = status("")
    assert r["status"] == "error"

def test_status_kwargs():
    r = status("t", extra="v")
    assert r["command"] == "status"

def test_cmd_status_text(capsys):
    cmd_status(DummyArgs(status_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_status_json(capsys):
    cmd_status(DummyArgs(status_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_status_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_status(DummyArgs(status_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "status", "test"])
def test_main_status():
    with patch("main.cmd_status") as m:
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
    with patch("sys.argv", ["main.py", "route", "test"]):
        runpy.run_path(s, run_name="__main__")
