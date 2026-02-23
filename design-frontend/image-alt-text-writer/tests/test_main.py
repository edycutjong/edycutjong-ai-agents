import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main

@patch('main.Scanner')
@patch('main.AltTextGenerator')
@patch('main.Reporter')
@patch('argparse.ArgumentParser.parse_args')
def test_main_flow(mock_args, MockReporter, MockGenerator, MockScanner):
    # Setup mocks
    mock_args.return_value = MagicMock(path="test.html", recursive=False, output_format="json", provider="openai")

    mock_scanner = MockScanner.return_value
    mock_scanner.scan_file.return_value = [
        MagicMock(src="test.jpg", filepath="test.html", context="ctx", to_dict=lambda: {"src": "test.jpg", "context": "ctx", "filepath": "test.html"})
    ]

    mock_generator = MockGenerator.return_value
    mock_generator.generate_alt_text.return_value = "Generated Alt"

    mock_reporter = MockReporter.return_value
    mock_reporter.generate_report.return_value = "report.json"

    with patch('main.get_image_data', return_value="base64data"):
        with patch('os.path.isfile', return_value=True):
             with patch('builtins.print'):
                main()

    mock_scanner.scan_file.assert_called_once()
    mock_generator.generate_alt_text.assert_called_once()
    mock_reporter.generate_report.assert_called_once()
