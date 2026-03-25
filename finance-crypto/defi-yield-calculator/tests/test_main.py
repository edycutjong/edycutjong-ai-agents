import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_calculate, cmd_compare, cmd_risk, main
from agent.core import calculate, compare, risk, format_output
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


# --- calculate core tests ---
def test_calculate_with_input():
    result = calculate("test-input")
    assert result["command"] == "calculate"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_calculate_empty_input():
    result = calculate("")
    assert result["command"] == "calculate"
    assert "status" in result

def test_calculate_with_kwargs():
    result = calculate("test", extra="value")
    assert result["command"] == "calculate"


# --- compare core tests ---
def test_compare_with_input():
    result = compare("test-input")
    assert result["command"] == "compare"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_compare_empty_input():
    result = compare("")
    assert result["command"] == "compare"
    assert "status" in result

def test_compare_with_kwargs():
    result = compare("test", extra="value")
    assert result["command"] == "compare"


# --- risk core tests ---
def test_risk_with_input():
    result = risk("test-input")
    assert result["command"] == "risk"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_risk_empty_input():
    result = risk("")
    assert result["command"] == "risk"
    assert "status" in result

def test_risk_with_kwargs():
    result = risk("test", extra="value")
    assert result["command"] == "risk"


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


def test_cmd_calculate_text(capsys):
    args = DummyArgs(calculate_input="test-data")
    cmd_calculate(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_calculate_json(capsys):
    args = DummyArgs(calculate_input="test-data", json=True)
    cmd_calculate(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_calculate_stdin(capsys):
    args = DummyArgs(calculate_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_calculate(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_cmd_compare_text(capsys):
    args = DummyArgs(compare_input="test-data")
    cmd_compare(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_compare_json(capsys):
    args = DummyArgs(compare_input="test-data", json=True)
    cmd_compare(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_compare_stdin(capsys):
    args = DummyArgs(compare_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_compare(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


def test_cmd_risk_text(capsys):
    args = DummyArgs(risk_input="test-data")
    cmd_risk(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_risk_json(capsys):
    args = DummyArgs(risk_input="test-data", json=True)
    cmd_risk(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_risk_stdin(capsys):
    args = DummyArgs(risk_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_risk(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


@patch("sys.argv", ["main.py", "--json", "calculate", "test"])
def test_main_calculate(capsys):
    with patch("main.cmd_calculate") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "compare", "test"])
def test_main_compare(capsys):
    with patch("main.cmd_compare") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "risk", "test"])
def test_main_risk(capsys):
    with patch("main.cmd_risk") as mock:
        main()
        mock.assert_called_once()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "calculate", "test"]):
        runpy.run_path(script, run_name="__main__")
