import sys
from unittest.mock import patch
from agent.main import main

def test_main_no_api_key(capsys, tmp_path):
    test_file = tmp_path / "dummy.html"
    test_file.write_text("<html></html>")
    
    test_args = ["agent/main.py", str(test_file)]
    with patch.object(sys, 'argv', test_args), \
         patch('os.getenv', return_value=None), \
         patch('agent.main.A11yFixer') as MockFixer, \
         patch('agent.main.generate_audit_report', return_value="a11y_report.html"):
        
        mock_instance = MockFixer.return_value
        mock_instance.scan_html.return_value = {"issues": [], "fixed_document": "<html></html>"}
        
        main()
        
        out, err = capsys.readouterr()
        assert "OPENAI_API_KEY not found" in out
        assert f"Scanning {test_file}" in out

def test_main_file_not_found(capsys):
    test_args = ["agent/main.py", "nonexistent_file_that_does_not_exist.html"]
    with patch.object(sys, 'argv', test_args), \
         patch('os.getenv', return_value="dummy_key"):
        
        main()
        
        out, err = capsys.readouterr()
        assert "Error: File 'nonexistent_file_that_does_not_exist.html' not found." in out

def test_main_with_api_key_and_fix(capsys, tmp_path):
    test_file = tmp_path / "dummy.html"
    test_file.write_text("<html></html>")
    
    test_args = ["agent/main.py", str(test_file), "--fix"]
    with patch.object(sys, 'argv', test_args), \
         patch('os.getenv', return_value="dummy_key"), \
         patch('agent.main.A11yFixer') as MockFixer, \
         patch('agent.main.generate_audit_report', return_value="a11y_report.html"):
        
        mock_instance = MockFixer.return_value
        mock_instance.scan_html.return_value = {"issues": [{"type": "error"}], "fixed_document": "<html>fixed</html>"}
        
        main()
        
        out, err = capsys.readouterr()
        assert "Audit complete: found 1 issues." in out
        
        fixed_file = tmp_path / "dummy_fixed.html"
        assert f"Patched HTML saved to {fixed_file}" in out
        assert fixed_file.read_text() == "<html>fixed</html>"

