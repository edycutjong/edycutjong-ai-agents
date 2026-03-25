import sys
import os
import pytest
from unittest.mock import patch
from agent.main import main

@patch('agent.main.load_dotenv')
def test_main_no_api_key(mock_load_dotenv, tmp_path, capsys):
    test_html = tmp_path / "test.html"
    test_html.write_text("<html></html>", encoding="utf-8")
    
    with patch.dict(os.environ, clear=True):
        with patch.object(sys, 'argv', ['agent', str(test_html)]):
            main()
    
    captured = capsys.readouterr()
    assert "Warning: OPENAI_API_KEY not found in environment" in captured.out

def test_main_file_not_found(capsys):
    with patch.object(sys, 'argv', ['agent', 'nonexistent.html']):
        main()
        
    captured = capsys.readouterr()
    assert "Error: File 'nonexistent.html' not found." in captured.out

def test_main_success(tmp_path, capsys):
    test_html = tmp_path / "test.html"
    test_html.write_text("<html></html>", encoding="utf-8")
    report_html = tmp_path / "report.html"
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch.object(sys, 'argv', ['agent', str(test_html), '--out', str(report_html)]):
            main()
            
    captured = capsys.readouterr()
    assert f"Scanning {test_html} for accessibility issues..." in captured.out
    assert f"Report saved to {report_html}" in captured.out

def test_main_fix(tmp_path, capsys):
    test_html = tmp_path / "test.html"
    test_html.write_text("<html></html>", encoding="utf-8")
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        with patch.object(sys, 'argv', ['agent', str(test_html), '--fix']):
            main()
            
    fixed_html = tmp_path / "test_fixed.html"
    assert fixed_html.exists()
    
    captured = capsys.readouterr()
    assert f"Patched HTML saved to {fixed_html}" in captured.out
