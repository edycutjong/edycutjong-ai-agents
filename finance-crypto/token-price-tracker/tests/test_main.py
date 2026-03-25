import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_track, cmd_alert, cmd_portfolio, main
from agent.core import track, alert, portfolio, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

# --- Config tests ---
def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")


# --- track core tests ---
def test_track_with_input():
    result = track("test-input")
    assert result["command"] == "track"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_track_empty_input():
    result = track("")
    assert result["command"] == "track"
    assert "status" in result

def test_track_with_kwargs():
    result = track("test", extra="value")
    assert result["command"] == "track"


# --- alert core tests ---
def test_alert_with_input():
    result = alert("test-input")
    assert result["command"] == "alert"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_alert_empty_input():
    result = alert("")
    assert result["command"] == "alert"
    assert "status" in result

def test_alert_with_kwargs():
    result = alert("test", extra="value")
    assert result["command"] == "alert"


# --- portfolio core tests ---
def test_portfolio_with_input():
    result = portfolio("test-input")
    assert result["command"] == "portfolio"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_portfolio_empty_input():
    result = portfolio("")
    assert result["command"] == "portfolio"
    assert "status" in result

def test_portfolio_with_kwargs():
    result = portfolio("test", extra="value")
    assert result["command"] == "portfolio"


# --- format_output tests ---
def test_format_output_text():
    result = {"command": "test", "status": "success", "data": {"key": "val"}}
    out = format_output(result, "text")
    assert "Command: test" in out
    assert "Status: success" in out

def test_format_output_json():
    result = {"command": "test", "status": "success", "data": {}}
    out = format_output(result, "json")
    parsed = json.loads(out)
    assert parsed["command"] == "test"

def test_format_output_error():
    result = {"command": "test", "status": "error", "error": "fail", "data": {}}
    out = format_output(result, "text")
    assert "Error:" in out


def test_cmd_track_text(capsys):
    args = DummyArgs(track_input="test-data")
    cmd_track(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_track_json(capsys):
    args = DummyArgs(track_input="test-data", json=True)
    cmd_track(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_track_stdin(capsys):
    args = DummyArgs(track_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_track(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_cmd_alert_text(capsys):
    args = DummyArgs(alert_input="test-data")
    cmd_alert(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_alert_json(capsys):
    args = DummyArgs(alert_input="test-data", json=True)
    cmd_alert(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_alert_stdin(capsys):
    args = DummyArgs(alert_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_alert(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_cmd_portfolio_text(capsys):
    args = DummyArgs(portfolio_input="test-data")
    cmd_portfolio(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_portfolio_json(capsys):
    args = DummyArgs(portfolio_input="test-data", json=True)
    cmd_portfolio(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_portfolio_stdin(capsys):
    args = DummyArgs(portfolio_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_portfolio(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


@patch("sys.argv", ["main.py", "--json", "track", "test"])
def test_main_track(capsys):
    with patch("main.cmd_track") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "alert", "test"])
def test_main_alert(capsys):
    with patch("main.cmd_alert") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "portfolio", "test"])
def test_main_portfolio(capsys):
    with patch("main.cmd_portfolio") as mock:
        main()
        mock.assert_called_once()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "track", "test"]):
        runpy.run_path(script, run_name="__main__")
