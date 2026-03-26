import os
import sys
import runpy
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main, run


def test_run():
    result = run("")
    assert "README Keeper" in result
    assert "README.md" in result


def test_run_with_input():
    result = run("some input")
    assert isinstance(result, str)


def test_main_no_readme():
    """Test main() early exit when README doesn't exist."""
    with patch("sys.argv", ["main.py", "--readme", "/nonexistent/README.md"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_main_no_readme_output(capsys):
    """Test main() prints usage info when README doesn't exist."""
    with patch("sys.argv", ["main.py", "--readme", "/nonexistent/README.md"]):
        try:
            main()
        except SystemExit:
            pass
    out = capsys.readouterr().out
    assert "README Keeper Agent" in out
    assert "not found" in out


def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "--readme", "/nonexistent/README.md"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass


import pytest
