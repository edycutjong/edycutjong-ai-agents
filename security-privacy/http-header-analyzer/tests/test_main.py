import pytest
import sys
import json
from io import StringIO
from unittest.mock import patch, mock_open

import main
from config import Config

def test_config():
    assert Config is not None

def test_cmd_analyze_stdin(monkeypatch, capsys):
    mock_headers = {"Server": "Apache"}
    monkeypatch.setattr("sys.stdin", StringIO(json.dumps(mock_headers)))
    
    class Args:
        file = "-"
    
    main.cmd_analyze(Args())
    captured = capsys.readouterr()
    assert "Server" in captured.out
    assert "Header Analysis" in captured.out

def test_cmd_analyze_file(capsys):
    mock_headers = {"Strict-Transport-Security": "max-age=31536000"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_headers))):
        class Args:
            file = "headers.json"
        main.cmd_analyze(Args())
        
    captured = capsys.readouterr()
    assert "Strict-Transport-Security" in captured.out

def test_main_block(capsys):
    mock_headers = {"Content-Security-Policy": "default-src 'self'"}
    with open("main.py", "r") as f:
        source_code = f.read()

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_headers))):
        with patch.object(sys, "argv", ["main.py", "analyze", "dummy.json"]):
            globals_dict = {"__name__": "__main__", "__file__": "main.py"}
            code = compile(source_code, "main.py", "exec")
            exec(code, globals_dict)
                
    captured = capsys.readouterr()
    assert "Content-Security-Policy" in captured.out
