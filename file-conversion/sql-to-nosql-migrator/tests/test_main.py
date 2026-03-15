import pytest
import os
import sys
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, migrate_command

def test_migrate_command_dir(tmp_path, capsys):
    f1 = tmp_path / "test1.sql"
    f1.write_text("SELECT 1;")
    d1 = tmp_path / "node_modules"
    d1.mkdir()
    f2 = d1 / "ignore.js"
    f2.write_text("console.log(1);")
    
    class Args:
        path = str(tmp_path)
        json = False
    
    migrate_command(Args())
    out, _ = capsys.readouterr()
    assert "1 items analyzed" in out
    assert "1 items analyzed" in out

def test_migrate_command_file(tmp_path, capsys):
    f = tmp_path / "test.sql"
    f.write_text("SELECT 1;")
    
    class Args:
        path = str(f)
        json = False
        
    migrate_command(Args())
    out, _ = capsys.readouterr()
    assert "1 items analyzed" in out

def test_migrate_command_invalid(capsys):
    class Args:
        path = "non_existent_folder"
        json = False
        
    migrate_command(Args())
    out, _ = capsys.readouterr()
    assert "Path not found" in out

def test_migrate_command_json(tmp_path, capsys):
    f = tmp_path / "test.sql"
    f.write_text("SELECT 1;")
    
    class Args:
        path = str(f)
        json = True
        
    migrate_command(Args())
    out, _ = capsys.readouterr()
    start = out.find("[\\n")
    if start == -1:
        start = out.find("[")
        # Ensure we skip the [bold cyan] output from rich by finding the actual JSON array
        while start != -1 and not out[start:].startswith("[\\n"):
            start = out.find("[", start + 1)
        if start == -1:
            start = out.find("[") # fallback
            
    data = json.loads(out[start:])
    assert len(data) == 1
    assert data[0]["file"] == str(f)

def test_main_cli():
    with patch("sys.argv", ["main.py", "migrate", "."]):
        with patch("main.migrate_command") as mock_cmd:
            main()
            mock_cmd.assert_called_once()
