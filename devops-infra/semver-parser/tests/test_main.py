import sys
import os
import runpy
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from agent.parser import satisfies_range

def test_config():
    c = Config()
    assert c is not None

def test_satisfies_range_exact():
    assert satisfies_range("1.0.0", "1.0.0")
    assert not satisfies_range("1.0.1", "1.0.0")

def test_main_parse(capsys):
    with patch("sys.argv", ["main.py", "parse", "1.2.3"]):
        runpy.run_path(os.path.join(os.path.dirname(__file__), '..', 'main.py'), run_name="__main__")
    
    captured = capsys.readouterr()
    assert "1.2.3" in captured.out
    assert "**Patch:** 3" in captured.out

def test_main_bump(capsys):
    with patch("sys.argv", ["main.py", "bump", "1.2.3", "--part", "minor"]):
        runpy.run_path(os.path.join(os.path.dirname(__file__), '..', 'main.py'), run_name="__main__")
    
    captured = capsys.readouterr()
    assert "1.3.0" in captured.out
    assert "**Minor:** 3" in captured.out
