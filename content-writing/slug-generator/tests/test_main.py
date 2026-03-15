import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import runpy

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config():
    import config
    assert hasattr(config, "Config")
    c = config.Config()

@patch('builtins.print')
def test_main_generate(mock_print):
    test_args = ['main.py', 'generate', 'Hello World!', '--sep', '_', '--max-length', '5']
    with patch.object(sys, 'argv', test_args):
        import main
        main.main()
        
    mock_print.assert_called_once()
    assert "hello" in str(mock_print.call_args)

@patch('main.main')
def test_main_block(mock_main):
    # Tests the if __name__ == "__main__": block
    with patch.object(sys, 'argv', ['main.py', '-h']):
        try:
            runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
        except SystemExit:
            pass # argparse -h calls sys.exit
