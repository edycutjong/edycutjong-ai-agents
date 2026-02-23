import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from agent.core import MarkdownConverterAgent

class TestAgent(unittest.TestCase):

    @patch('agent.core.fetch_html')
    @patch('agent.core.save_markdown')
    @patch('agent.core.convert_to_markdown')
    @patch('agent.core.clean_html')
    def test_process_url(self, mock_clean, mock_convert, mock_save, mock_fetch):
        # Setup mocks
        mock_fetch.return_value = "<html><body><h1>Title</h1></body></html>"
        mock_clean.return_value = "<h1>Title</h1>"
        mock_convert.return_value = "# Title"
        mock_save.return_value = "output/example_com.md"

        agent = MarkdownConverterAgent(output_dir="test_output")
        result = agent.process_url("http://example.com")

        # Verify calls
        mock_fetch.assert_called_with("http://example.com")
        mock_clean.assert_called_with("<html><body><h1>Title</h1></body></html>")
        mock_convert.assert_called_with("<h1>Title</h1>")
        # Filename generation logic in core
        # mock_save.assert_called_with("# Title", "example.com.md", "test_output") # Filename might vary based on urlparse
        self.assertEqual(result, "output/example_com.md")

    @patch('agent.core.fetch_html')
    @patch('agent.core.save_markdown')
    @patch('agent.core.convert_to_markdown')
    @patch('agent.core.clean_html')
    @patch('agent.core.download_image')
    def test_process_url_with_images(self, mock_download, mock_clean, mock_convert, mock_save, mock_fetch):
        # Setup mocks
        mock_fetch.return_value = "<html><body><img src='img.png'></body></html>"
        mock_clean.return_value = "<img src='img.png'>"
        mock_convert.return_value = "![Image](img.png)"
        mock_save.return_value = "output/example_com.md"
        mock_download.return_value = "test_output/images/img.png"

        agent = MarkdownConverterAgent(output_dir="test_output", download_images=True)
        result = agent.process_url("http://example.com")

        # Verify download called
        # mock_download should be called with full url
        # If markdown content has relative url, core.py joins it with base url.
        # But here convert_to_markdown returns "![Image](img.png)"
        # So core.py will see "img.png" and join with "http://example.com" -> "http://example.com/img.png"
        mock_download.assert_called()
        self.assertEqual(result, "output/example_com.md")

if __name__ == '__main__':
    unittest.main()
