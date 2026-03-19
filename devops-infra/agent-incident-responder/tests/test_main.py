import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main


def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")  # pragma: no cover
    with patch("sys.argv", ["main.py"]):  # pragma: no cover
        try:  # pragma: no cover
            runpy.run_path(script_path, run_name="__main__")  # pragma: no cover
        except SystemExit:  # pragma: no cover
            pass  # pragma: no cover
