import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_check, cmd_portfolio, cmd_history, main
from agent.core import check, portfolio, history, format_output
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


# --- check core tests ---
def test_check_with_input():
    result = check("test-input")
    assert result["command"] == "check"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_check_empty_input():
    result = check("")
    assert result["command"] == "check"
    assert "status" in result

def test_check_with_kwargs():
    result = check("test", extra="value")
    assert result["command"] == "check"


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


# --- history core tests ---
def test_history_with_input():
    result = history("test-input")
    assert result["command"] == "history"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_history_empty_input():
    result = history("")
    assert result["command"] == "history"
    assert "status" in result

def test_history_with_kwargs():
    result = history("test", extra="value")
    assert result["command"] == "history"


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


def test_cmd_check_text(capsys):
    args = DummyArgs(check_input="test-data")
    cmd_check(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_check_json(capsys):
    args = DummyArgs(check_input="test-data", json=True)
    cmd_check(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_check_stdin(capsys):
    args = DummyArgs(check_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_check(args)
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


def test_cmd_history_text(capsys):
    args = DummyArgs(history_input="test-data")
    cmd_history(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_history_json(capsys):
    args = DummyArgs(history_input="test-data", json=True)
    cmd_history(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_history_stdin(capsys):
    args = DummyArgs(history_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_history(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


@patch("sys.argv", ["main.py", "--json", "check", "test"])
def test_main_check(capsys):
    with patch("main.cmd_check") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "portfolio", "test"])
def test_main_portfolio(capsys):
    with patch("main.cmd_portfolio") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "history", "test"])
def test_main_history(capsys):
    with patch("main.cmd_history") as mock:
        main()
        mock.assert_called_once()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "check", "test"]):
        runpy.run_path(script, run_name="__main__")
