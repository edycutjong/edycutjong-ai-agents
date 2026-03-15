import os
import sys
from unittest.mock import patch
import runpy
from io import StringIO

import main

def test_cmd_lookup():
    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        args = main.argparse.Namespace(ip="8.8.8.8", func=main.cmd_lookup)
        main.cmd_lookup(args)
        out = mock_out.getvalue()
        assert "Google" in out

def test_main_cli():
    with patch("sys.argv", ["main.py", "lookup", "8.8.8.8"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            main.main()
            out = mock_out.getvalue()
            assert "Google" in out

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "lookup", "8.8.8.8"]):
        runpy.run_path(script_path, run_name="__main__")
