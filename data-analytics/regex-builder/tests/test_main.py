import pytest
import sys
import os
from unittest.mock import patch
import runpy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config():
    import config
    assert hasattr(config, "Config")

@patch('builtins.print')
def test_main_test_match(mock_print):
    # Test valid regex with matches
    test_args = ['main.py', 'test', 'foo', 'foobar']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
    mock_print.assert_called_once()
    assert "\u2705 **1 matches found**" in mock_print.call_args[0][0]

@patch('builtins.print')
def test_main_test_stdin(mock_print):
    # Test text from stdin
    test_args = ['main.py', 'test', 'foo', '-']
    with patch.object(sys, 'argv', test_args):
        with patch('sys.stdin.read', return_value='foobar'):
            import main
            main.main()
    mock_print.assert_called_once()
    assert "\u2705 **1 matches found**" in mock_print.call_args[0][0]

@patch('builtins.print')
def test_main_test_invalid(mock_print):
    # Test invalid regex (covers line 85 and error branch)
    test_args = ['main.py', 'test', '[', 'text']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
    mock_print.assert_called_once()
    assert "\u274c Invalid:" in mock_print.call_args[0][0]

@patch('builtins.print')
def test_main_list(mock_print):
    test_args = ['main.py', 'list']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
    assert mock_print.call_count > 0

@patch('builtins.print')
def test_main_explain(mock_print):
    # Test explain regex (covers capture group, set, quantifier)
    test_args = ['main.py', 'explain', '([a-z]){3}']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
    mock_print.assert_called_once()
    output = mock_print.call_args[0][0]
    assert "capture group" in output
    assert "character set" in output
    assert "repeat 3 times" in output

def test_result_to_dict():
    from agent.builder import TestResult
    tr = TestResult(pattern="a", text="a", matches=["a"], match_count=1)
    d = tr.to_dict()
    assert d["match_count"] == 1
    assert "matches" in d

def test_main_block():
    with patch.object(sys, 'argv', ['main.py', '-h']):
        try:
            runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
        except SystemExit as e:
            assert e.code == 0
