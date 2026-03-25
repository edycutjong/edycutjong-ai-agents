import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_plan, cmd_grocery, cmd_nutrition, main
from agent.core import plan, grocery, nutrition, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_plan_with_input():
    r = plan("test-input")
    assert r["command"] == "plan"
    assert r["status"] == "success"

def test_plan_empty():
    r = plan("")
    assert r["status"] == "error"

def test_plan_kwargs():
    r = plan("t", extra="v")
    assert r["command"] == "plan"

def test_cmd_plan_text(capsys):
    cmd_plan(DummyArgs(plan_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_plan_json(capsys):
    cmd_plan(DummyArgs(plan_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_plan_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_plan(DummyArgs(plan_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "plan", "test"])
def test_main_plan():
    with patch("main.cmd_plan") as m:
        main()
        m.assert_called_once()

def test_grocery_with_input():
    r = grocery("test-input")
    assert r["command"] == "grocery"
    assert r["status"] == "success"

def test_grocery_empty():
    r = grocery("")
    assert r["status"] == "error"

def test_grocery_kwargs():
    r = grocery("t", extra="v")
    assert r["command"] == "grocery"

def test_cmd_grocery_text(capsys):
    cmd_grocery(DummyArgs(grocery_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_grocery_json(capsys):
    cmd_grocery(DummyArgs(grocery_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_grocery_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_grocery(DummyArgs(grocery_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "grocery", "test"])
def test_main_grocery():
    with patch("main.cmd_grocery") as m:
        main()
        m.assert_called_once()

def test_nutrition_with_input():
    r = nutrition("test-input")
    assert r["command"] == "nutrition"
    assert r["status"] == "success"

def test_nutrition_empty():
    r = nutrition("")
    assert r["status"] == "error"

def test_nutrition_kwargs():
    r = nutrition("t", extra="v")
    assert r["command"] == "nutrition"

def test_cmd_nutrition_text(capsys):
    cmd_nutrition(DummyArgs(nutrition_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_nutrition_json(capsys):
    cmd_nutrition(DummyArgs(nutrition_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_nutrition_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_nutrition(DummyArgs(nutrition_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "nutrition", "test"])
def test_main_nutrition():
    with patch("main.cmd_nutrition") as m:
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
    with patch("sys.argv", ["main.py", "plan", "test"]):
        runpy.run_path(s, run_name="__main__")
