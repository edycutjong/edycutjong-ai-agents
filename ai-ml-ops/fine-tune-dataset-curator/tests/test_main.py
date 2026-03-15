import pytest
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

import main
from config import Config

def test_main_config_error(capsys, monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", None)
    with patch("sys.argv", ["main.py", "dummy query"]):
        with pytest.raises(SystemExit) as e:
            main.main()
        assert e.value.code == 1

@patch("main.create_curator_agent")
def test_main_success(mock_create_agent, capsys):
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {"output": "Mocked Output"}
    mock_create_agent.return_value = mock_agent
    
    with patch("sys.argv", ["main.py", "dummy query"]):
        with patch.object(Config, "OPENAI_API_KEY", "dummy"): # To avoid config validation error if set to None
            main.main()
            
    captured = capsys.readouterr()
    assert "Mocked Output" in captured.out

@patch("main.create_curator_agent")
def test_main_exception(mock_create_agent, capsys):
    mock_agent = MagicMock()
    mock_agent.invoke.side_effect = Exception("Test Exception")
    mock_create_agent.return_value = mock_agent
    
    with patch("sys.argv", ["main.py", "dummy query"]):
        with patch.object(Config, "OPENAI_API_KEY", "dummy"):
            main.main()
            
    captured = capsys.readouterr()
    assert "An error occurred: Test Exception" in captured.out

@patch("main.create_curator_agent")
def test_main_exception_verbose(mock_create_agent, capsys):
    mock_agent = MagicMock()
    mock_agent.invoke.side_effect = Exception("Test Exception")
    mock_create_agent.return_value = mock_agent
    
    with patch("sys.argv", ["main.py", "dummy query", "--verbose"]):
        with patch.object(Config, "OPENAI_API_KEY", "dummy"):
            main.main()
            
    captured = capsys.readouterr()
    assert "Traceback" in captured.err or "Traceback" in captured.out

import runpy

def test_main_block(capsys):
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {"output": "Mocked Block Output"}
    
    with patch.object(sys, "argv", ["main.py", "dummy query"]):
        with patch.object(Config, "OPENAI_API_KEY", "dummy"):
            with patch("agent.curator.create_curator_agent", return_value=mock_agent):
                runpy.run_path("main.py", run_name="__main__")
                
    captured = capsys.readouterr()
    assert "Mocked Block Output" in captured.out
