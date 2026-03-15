import os
import sys
import json
from unittest.mock import patch, mock_open
import runpy
from io import StringIO

import main

def test_cmd_validate_stdin():
    data = {"name": "test", "age": 30}
    with patch("sys.stdin", StringIO(json.dumps(data))):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            args = main.argparse.Namespace(file="-", status=200, func=main.cmd_validate)
            main.cmd_validate(args)
            out = mock_out.getvalue()
            assert "✅ All validations passed!" in out

def test_cmd_validate_file():
    data = {"name": "test", "age": 30}
    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            args = main.argparse.Namespace(file="dummy.json", status=400, func=main.cmd_validate)
            main.cmd_validate(args)
            out = mock_out.getvalue()
            assert "### Warnings" in out
            assert "HTTP status 400 indicates an error" in out

def test_main_cli():
    data = {"name": "test"}
    with patch("sys.argv", ["main.py", "validate", "-"]):
        with patch("sys.stdin", StringIO(json.dumps(data))):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                main.main()
                out = mock_out.getvalue()
                assert "✅ All validations passed!" in out

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    data = {"name": "test"}
    with patch("sys.argv", ["main.py", "validate", "-"]):
        with patch("sys.stdin", StringIO(json.dumps(data))):
            runpy.run_path(script_path, run_name="__main__")
