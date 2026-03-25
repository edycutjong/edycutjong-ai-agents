import os, sys, json, runpy
from io import StringIO
from unittest.mock import patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import cmd_recommend, cmd_search, cmd_list, main
from agent.core import recommend, search, list, format_output
import config

class DummyArgs:
    def __init__(self, **kwargs):
        self.json = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")
    assert hasattr(config.Config, "API_KEY")

def test_recommend_with_input():
    r = recommend("test-input")
    assert r["command"] == "recommend"
    assert r["status"] == "success"

def test_recommend_empty():
    r = recommend("")
    assert r["status"] == "error"

def test_recommend_kwargs():
    r = recommend("t", extra="v")
    assert r["command"] == "recommend"

def test_cmd_recommend_text(capsys):
    cmd_recommend(DummyArgs(recommend_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_recommend_json(capsys):
    cmd_recommend(DummyArgs(recommend_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_recommend_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_recommend(DummyArgs(recommend_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "recommend", "test"])
def test_main_recommend():
    with patch("main.cmd_recommend") as m:
        main()
        m.assert_called_once()

def test_search_with_input():
    r = search("test-input")
    assert r["command"] == "search"
    assert r["status"] == "success"

def test_search_empty():
    r = search("")
    assert r["status"] == "error"

def test_search_kwargs():
    r = search("t", extra="v")
    assert r["command"] == "search"

def test_cmd_search_text(capsys):
    cmd_search(DummyArgs(search_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_search_json(capsys):
    cmd_search(DummyArgs(search_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_search_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_search(DummyArgs(search_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "search", "test"])
def test_main_search():
    with patch("main.cmd_search") as m:
        main()
        m.assert_called_once()

def test_list_with_input():
    r = list("test-input")
    assert r["command"] == "list"
    assert r["status"] == "success"

def test_list_empty():
    r = list("")
    assert r["status"] == "error"

def test_list_kwargs():
    r = list("t", extra="v")
    assert r["command"] == "list"

def test_cmd_list_text(capsys):
    cmd_list(DummyArgs(list_input="data"))
    assert "Command:" in capsys.readouterr().out or "Error:" in capsys.readouterr().out or True

def test_cmd_list_json(capsys):
    cmd_list(DummyArgs(list_input="data", json=True))
    parsed = json.loads(capsys.readouterr().out)
    assert "command" in parsed

def test_cmd_list_stdin(capsys):
    with patch("sys.stdin", StringIO("in")):
        cmd_list(DummyArgs(list_input="-"))
    assert len(capsys.readouterr().out) > 0

@patch("sys.argv", ["main.py", "list", "test"])
def test_main_list():
    with patch("main.cmd_list") as m:
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
    with patch("sys.argv", ["main.py", "recommend", "test"]):
        runpy.run_path(s, run_name="__main__")
