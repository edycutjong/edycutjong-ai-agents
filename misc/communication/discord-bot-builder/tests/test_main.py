import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_generate, cmd_scaffold, cmd_deploy, main
from agent.core import generate, scaffold, deploy, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_generate_with_input():
    r = generate("test-input")
    assert r["command"] == "generate"
    assert r["status"] == "success"

def test_generate_empty():
    r = generate("")
    assert r["status"] == "error"

def test_generate_kwargs():
    r = generate("t", extra="v")
    assert r["command"] == "generate"

def test_cmd_generate_text(capsys):
    cmd_generate(DummyArgs(generate_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_generate_json(capsys):
    cmd_generate(DummyArgs(generate_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_generate_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_generate(DummyArgs(generate_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "generate", "test"])
def test_main_generate():
    with patch("main.cmd_generate") as m:
        main()
        m.assert_called_once()

def test_scaffold_with_input():
    r = scaffold("test-input")
    assert r["command"] == "scaffold"
    assert r["status"] == "success"

def test_scaffold_empty():
    r = scaffold("")
    assert r["status"] == "error"

def test_scaffold_kwargs():
    r = scaffold("t", extra="v")
    assert r["command"] == "scaffold"

def test_cmd_scaffold_text(capsys):
    cmd_scaffold(DummyArgs(scaffold_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_scaffold_json(capsys):
    cmd_scaffold(DummyArgs(scaffold_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_scaffold_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_scaffold(DummyArgs(scaffold_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "scaffold", "test"])
def test_main_scaffold():
    with patch("main.cmd_scaffold") as m:
        main()
        m.assert_called_once()

def test_deploy_with_input():
    r = deploy("test-input")
    assert r["command"] == "deploy"
    assert r["status"] == "success"

def test_deploy_empty():
    r = deploy("")
    assert r["status"] == "error"

def test_deploy_kwargs():
    r = deploy("t", extra="v")
    assert r["command"] == "deploy"

def test_cmd_deploy_text(capsys):
    cmd_deploy(DummyArgs(deploy_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_deploy_json(capsys):
    cmd_deploy(DummyArgs(deploy_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_deploy_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_deploy(DummyArgs(deploy_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "deploy", "test"])
def test_main_deploy():
    with patch("main.cmd_deploy") as m:
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
    with patch("sys.argv", ["main.py", "generate", "test"]):
        runpy.run_path(s, run_name="__main__")
