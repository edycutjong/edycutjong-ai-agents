import pytest
from unittest.mock import patch, MagicMock, PropertyMock
import sys
import os
import runpy

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main
from agent.scanner import ImageInfo

@pytest.fixture
def mock_scanner():
    with patch('main.Scanner') as mock:
        yield mock

@pytest.fixture
def mock_generator():
    with patch('main.AltTextGenerator') as mock:
        yield mock

@pytest.fixture
def mock_reporter():
    with patch('main.Reporter') as mock:
        yield mock

def create_mock_args(path="test.html", recursive=False, output_format="json", provider="openai"):
    mock = MagicMock()
    mock.path = path
    mock.recursive = recursive
    mock.output_format = output_format
    mock.provider = provider
    return mock

@patch('argparse.ArgumentParser.parse_args')
@patch('main.RICH_AVAILABLE', True)
@patch('main.get_image_data', return_value="base64data")
@patch('os.path.isfile', return_value=True)
def test_main_flow_rich(mock_isfile, mock_get_image_data, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args()
    
    mock_scan_instance = mock_scanner.return_value
    images = [ImageInfo("test.jpg", None, "ctx", "test.html")] * 6 # To trigger the >5 images logic
    mock_scan_instance.scan_file.return_value = images
    
    mock_gen_instance = mock_generator.return_value
    mock_gen_instance.generate_alt_text.return_value = "Generated Alt"
    
    mock_rep_instance = mock_reporter.return_value
    mock_rep_instance.generate_report.return_value = "report.json"
    
    with patch('main.Console') as mock_console:
        main()
        mock_console.return_value.print.assert_called()

@patch('argparse.ArgumentParser.parse_args')
@patch('main.RICH_AVAILABLE', False)
@patch('main.get_image_data', return_value="base64data")
@patch('os.path.isfile', return_value=True)
def test_main_flow_no_rich(mock_isfile, mock_get_image_data, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args()
    
    mock_scan_instance = mock_scanner.return_value
    mock_scan_instance.scan_file.return_value = [ImageInfo("test.jpg", None, "ctx", "test.html")]
    
    mock_gen_instance = mock_generator.return_value
    mock_gen_instance.generate_alt_text.return_value = "Generated Alt"
    
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called()

@patch('argparse.ArgumentParser.parse_args')
@patch('main.RICH_AVAILABLE', False)
@patch('main.get_image_data', return_value=None)
@patch('os.path.isfile', return_value=True)
def test_main_flow_no_image_data(mock_isfile, mock_get_image_data, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args()
    mock_scanner.return_value.scan_file.return_value = [ImageInfo("test.jpg", None, "ctx", "test.html")]
    
    with patch('builtins.print'):
        main()

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isfile', return_value=False)
@patch('os.path.isdir', return_value=True)
def test_main_flow_directory(mock_isdir, mock_isfile, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args(path="testdir", recursive=True)
    mock_scanner.return_value.scan_directory.return_value = []
    
    with patch('builtins.print'):
        main()
        mock_scanner.return_value.scan_directory.assert_called_once_with("testdir", recursive=True)

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isfile', return_value=False)
@patch('os.path.isdir', return_value=False)
def test_main_invalid_path(mock_isdir, mock_isfile, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args()
    with patch('main.RICH_AVAILABLE', True):
        with patch('main.Console') as mock_console:
            main()
    with patch('main.RICH_AVAILABLE', False):
        with patch('builtins.print'):
            main()

@patch('argparse.ArgumentParser.parse_args')
def test_main_warnings_keys_missing_openai(mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args(provider="openai")
    with patch('config.config.OPENAI_API_KEY', None):
        with patch('main.RICH_AVAILABLE', True):
            with patch('rich.console.Console'):
                main()
        with patch('main.RICH_AVAILABLE', False):
            with patch('builtins.print'):
                main()

@patch('argparse.ArgumentParser.parse_args')
def test_main_warnings_keys_missing_google(mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args(provider="google")
    with patch('config.config.GEMINI_API_KEY', None):
        with patch('main.RICH_AVAILABLE', True):
            with patch('rich.console.Console'):
                main()
        with patch('main.RICH_AVAILABLE', False):
            with patch('builtins.print'):
                main()

@patch('argparse.ArgumentParser.parse_args')
def test_main_generator_exception(mock_args, mock_scanner, mock_reporter):
    mock_args.return_value = create_mock_args()
    with patch('main.AltTextGenerator', side_effect=Exception("Generator Error")):
        with patch('main.RICH_AVAILABLE', True):
            with patch('rich.console.Console'):
                main()
        with patch('main.RICH_AVAILABLE', False):
            with patch('builtins.print'):
                main()

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isfile', return_value=True)
def test_main_no_results(mock_isfile, mock_args, mock_scanner, mock_generator, mock_reporter):
    mock_args.return_value = create_mock_args()
    mock_scanner.return_value.scan_file.return_value = []
    
    with patch('main.RICH_AVAILABLE', True):
        with patch('rich.console.Console'):
            main()
    with patch('main.RICH_AVAILABLE', False):
        with patch('builtins.print'):
            main()

def test_main_exception_in_provider_check():
    with patch('argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.Scanner'), \
         patch('main.AltTextGenerator'), \
         patch('main.Reporter'), \
         patch('main.Console'):
        mock_args.return_value = MagicMock()
        type(mock_args.return_value).provider = PropertyMock(side_effect=Exception("Test exception"))
        mock_args.return_value.path = "test.html"
        main()

def test_main_block():
    with patch('sys.argv', ['main.py', 'test.html']):
        with open('main.py') as f:
            code = compile(f.read(), 'main.py', 'exec')
            # Provide necessary builtins and __file__ to avoid NameError
            ctx = {'__name__': '__main__', '__file__': 'main.py'}
            import builtins
            ctx['__builtins__'] = builtins.__dict__
            exec(code, ctx)

def test_imports_rich_fallback():
    # To test the import fallback, we need to temporarily hide `rich` from sys.modules
    import sys
    import importlib
    
    with patch.dict('sys.modules', {'rich.console': None}):
        if 'main' in sys.modules:
            del sys.modules['main']
        import main
        assert main.RICH_AVAILABLE is False
        
    # restore main module properly
    if 'main' in sys.modules:
        del sys.modules['main']
    importlib.import_module('main')
