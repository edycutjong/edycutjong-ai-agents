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
@patch('builtins.open', new_callable=mock_open, read_data='#BadHeading\n\nCheck this bare link http://example.com')
def test_main_lint_file(mock_file, mock_print):
    test_args = ['main.py', 'lint', 'test.md']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
        
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    # Covers severity == "error" in format_result_markdown (line 73-74)
    assert "\u274c Line 1: [heading-style]" in output
    # Covers bare URLs (line 57)
    assert "\u26a0\ufe0f Line 3: [no-bare-urls]" in output

@patch('builtins.print')
def test_main_lint_stdin(mock_print):
    test_args = ['main.py', 'lint', '-']
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdin.read', return_value='# Good Heading\n\nText.'):
            import main
            main.main()
            
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "Markdown Lint \u2705" in output

def test_main_block():
    with patch.object(sys, 'argv', ['main.py', '-h']):
        try:
            runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
        except SystemExit as e:
            assert e.code == 0
