import os
import sys
import runpy
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "test"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except SystemExit:
            pass
