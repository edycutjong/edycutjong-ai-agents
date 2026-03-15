import pytest
import sys
import os
from unittest.mock import patch, mock_open
import runpy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config():
    import config
    assert hasattr(config, "Config")

@patch('builtins.print')
@patch('builtins.open', new_callable=mock_open, read_data='invalid_line\nVALID=1')
def test_main_validate_file(mock_file, mock_print):
    test_args = ['main.py', 'validate', 'test.env']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
        
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "Issues" in output
    assert "Line 1:" in output

@patch('builtins.print')
def test_main_validate_stdin(mock_print):
    test_args = ['main.py', 'validate', '-']
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdin.read', return_value='VALID=1\n'):
            import main
            main.main()
            
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "**Variables:** 1" in output
    assert "Issues" not in output

@patch('main.main')
def test_main_block(mock_main):
    with patch.object(sys, 'argv', ['main.py', '-h']):
        try:
            runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
        except SystemExit:
            pass
