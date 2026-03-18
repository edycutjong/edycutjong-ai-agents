import os
import sys
import runpy
from io import StringIO
import pytest


import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except SystemExit:
            pass
