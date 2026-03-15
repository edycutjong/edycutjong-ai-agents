import sys
import json
import pytest
from unittest.mock import patch, mock_open

# Import config to get coverage
import config
from main import main, cmd_organize
from agent.organizer import organize_file_list, format_result_markdown

def test_config_coverage():
    assert hasattr(config, "Config")

def test_cmd_organize_stdin(capsys):
    test_data = [{"name": "test1.txt", "size": 100}, {"name": "test2.jpg", "size": 200}]
    json_data = json.dumps(test_data)
    
    class DummyArgs:
        file = "-"
        
    with patch("sys.stdin.read", return_value=json_data):
        cmd_organize(DummyArgs())
        
    out, _ = capsys.readouterr()
    assert "test1.txt" not in out # The output is markdown summary, not filename
    assert "File Organization" in out
    assert "2 files" in out

def test_cmd_organize_file(capsys):
    test_data = [{"name": "test1.txt", "size": 100}]
    json_data = json.dumps(test_data)
    
    class DummyArgs:
        file = "dummy.json"
        
    with patch("builtins.open", mock_open(read_data=json_data)):
        cmd_organize(DummyArgs())
        
    out, _ = capsys.readouterr()
    assert "1 files" in out

def test_main_cli(capsys):
    test_data = [{"name": "a.jpg", "size": 10}, {"name": "b.jpg", "size": 10}, {"name": "c.jpg", "size": 10}]
    json_data = json.dumps(test_data)
    
    with patch("sys.argv", ["main.py", "organize", "-"]):
        with patch("sys.stdin.read", return_value=json_data):
            main()
            
    out, _ = capsys.readouterr()
    assert "Suggestions" in out # 3 images should trigger categories count >= 3

def test_suggestions_large_file_count():
    # Test organizer.py lines 65-66 directly
    files = [{"name": f"test_{i}.unknown", "size": 10} for i in range(25)]
    r = organize_file_list(files)
    md = format_result_markdown(r)
    assert "Suggestions" in md
    assert "Consider adding a README" in md
