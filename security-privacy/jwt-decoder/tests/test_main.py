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
def test_main_decode(mock_print):
    test_args = ['main.py', 'decode', 'fake.jwt.token']
    
    with patch.object(sys, 'argv', test_args):
        with patch('agent.decoder.decode_jwt', return_value={'header': {}, 'payload': {}, 'signature': 'test', 'is_valid': True}):
            with patch('agent.decoder.format_result_markdown', return_value='Formatted Markdown'):
                import main
                main.main()
                
    mock_print.assert_called_once_with('Formatted Markdown')

def test_main_block():
    with patch.object(sys, 'argv', ['main.py', '-h']):
        try:
            runpy.run_path(os.path.join(os.path.dirname(__file__), "..", "main.py"), run_name="__main__")
        except SystemExit as e:
            assert e.code == 0
