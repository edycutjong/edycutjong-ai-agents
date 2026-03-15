"""Tests for monorepo tools."""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from agent.tools import make_directory, write_file_content, run_command


def test_make_directory(tmp_path):
    """Test creating a directory."""
    target = str(tmp_path / "sub" / "deep")
    make_directory(target)
    assert Path(target).exists()


def test_write_file_content(tmp_path):
    """Test writing content to a file."""
    target = str(tmp_path / "sub" / "file.txt")
    write_file_content(target, "hello world")
    assert Path(target).read_text() == "hello world"


def test_run_command_success():
    """Cover tools.py lines 19-28: successful command execution."""
    returncode, stdout, stderr = run_command("echo hello")
    assert returncode == 0
    assert "hello" in stdout


def test_run_command_failure():
    """Cover tools.py lines 19-28: failed command."""
    returncode, stdout, stderr = run_command("false")
    assert returncode != 0


def test_run_command_exception():
    """Cover tools.py lines 29-30: command exception."""
    with patch("agent.tools.subprocess.run", side_effect=Exception("cmd error")):
        returncode, stdout, stderr = run_command("bad")
        assert returncode == 1
        assert "cmd error" in stderr
