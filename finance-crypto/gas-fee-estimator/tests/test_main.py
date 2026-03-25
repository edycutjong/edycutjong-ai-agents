import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_estimate, cmd_compare, cmd_optimal, main
from agent.core import estimate, compare, optimal, format_output
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


# --- estimate core tests ---
def test_estimate_with_input():
    result = estimate("test-input")
    assert result["command"] == "estimate"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_estimate_empty_input():
    result = estimate("")
    assert result["command"] == "estimate"
    assert "status" in result

def test_estimate_with_kwargs():
    result = estimate("test", extra="value")
    assert result["command"] == "estimate"


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


# --- optimal core tests ---
def test_optimal_with_input():
    result = optimal("test-input")
    assert result["command"] == "optimal"
    assert result["status"] == "success"
    assert result["input"] == "test-input"

def test_optimal_empty_input():
    result = optimal("")
    assert result["command"] == "optimal"
    assert "status" in result

def test_optimal_with_kwargs():
    result = optimal("test", extra="value")
    assert result["command"] == "optimal"


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


def test_cmd_estimate_text(capsys):
    args = DummyArgs(estimate_input="test-data")
    cmd_estimate(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_estimate_json(capsys):
    args = DummyArgs(estimate_input="test-data", json=True)
    cmd_estimate(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_estimate_stdin(capsys):
    args = DummyArgs(estimate_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_estimate(args)
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


def test_cmd_optimal_text(capsys):
    args = DummyArgs(optimal_input="test-data")
    cmd_optimal(args)
    captured = capsys.readouterr()
    assert "Command:" in captured.out or "Error:" in captured.out

def test_cmd_optimal_json(capsys):
    args = DummyArgs(optimal_input="test-data", json=True)
    cmd_optimal(args)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert "command" in parsed

def test_cmd_optimal_stdin(capsys):
    args = DummyArgs(optimal_input="-")
    with patch("sys.stdin", StringIO("stdin-data")):
        cmd_optimal(args)
    captured = capsys.readouterr()
    assert len(captured.out) > 0


@patch("sys.argv", ["main.py", "--json", "estimate", "test"])
def test_main_estimate(capsys):
    with patch("main.cmd_estimate") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "compare", "test"])
def test_main_compare(capsys):
    with patch("main.cmd_compare") as mock:
        main()
        mock.assert_called_once()


@patch("sys.argv", ["main.py", "--json", "optimal", "test"])
def test_main_optimal(capsys):
    with patch("main.cmd_optimal") as mock:
        main()
        mock.assert_called_once()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "estimate", "test"]):
        runpy.run_path(script, run_name="__main__")
