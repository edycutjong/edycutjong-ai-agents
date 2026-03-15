import pytest
import runpy
import sys
import os
from unittest.mock import patch, MagicMock
from agent.extractor import TextExtractor
from agent.reviewer import ReviewerAgent
from agent.report import ReportGenerator

def test_main_file(capsys, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.touch()
        
    with patch.object(sys, "argv", ["main.py", str(test_file)]):
        with patch.object(TextExtractor, "extract_text_from_file", return_value=[{"text": "test copy"}]):
            with patch.object(ReviewerAgent, "review_items", return_value=[{"text": "test copy", "issues": {"Clarity": "Issue"}}]):
                with patch.object(ReportGenerator, "save_report") as mock_save:
                    runpy.run_path("main.py", run_name="__main__")
                    assert mock_save.called

def test_main_dir(capsys, tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "test1.txt").touch()
    
    with patch.object(sys, "argv", ["main.py", str(test_dir)]):
        with patch.object(TextExtractor, "extract_text_from_file", return_value=[]):
            runpy.run_path("main.py", run_name="__main__")
            
    captured = capsys.readouterr()
    assert "No issues found" in captured.out

def test_main_not_exist(capsys):
    with patch.object(sys, "argv", ["main.py", "does_not_exist"]):
        with pytest.raises(SystemExit):
            runpy.run_path("main.py", run_name="__main__")
            
    captured = capsys.readouterr()
    assert "does not exist" in captured.out

def test_main_exception(capsys, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.touch()
    
    with patch.object(sys, "argv", ["main.py", str(test_file)]):
        with patch.object(TextExtractor, "extract_text_from_file", side_effect=Exception("ExtractError")):
            runpy.run_path("main.py", run_name="__main__")
            
    captured = capsys.readouterr()
    assert "ExtractError" in captured.out
