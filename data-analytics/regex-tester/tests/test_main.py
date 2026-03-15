import os
import sys
from unittest.mock import patch
import runpy
from io import StringIO

import main
import config

def test_config():
    assert config.Config is not None

def test_cmd_test():
    with patch("sys.stdout", new_callable=StringIO) as mock_out:
        args = main.argparse.Namespace(pattern="a.*b", text="acb", flags="", func=main.cmd_test)
        main.cmd_test(args)
        out = mock_out.getvalue()
        assert "**Matches:** 1" in out

def test_main_cli():
    with patch("sys.argv", ["main.py", "test", "a.*b", "acb"]):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            main.main()
            out = mock_out.getvalue()
            assert "**Matches:** 1" in out

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "test", "a.*b", "acb"]):
        with patch("sys.stdout", new_callable=StringIO):
            runpy.run_path(script_path, run_name="__main__")
