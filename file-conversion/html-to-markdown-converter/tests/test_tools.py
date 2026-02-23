import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import requests

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from agent.tools import fetch_html, clean_html, convert_to_markdown, extract_images

class TestTools(unittest.TestCase):

    @patch('agent.tools.requests.get')
    def test_fetch_html_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body>Hello</body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_html("http://example.com")
        self.assertEqual(result, "<html><body>Hello</body></html>")

    @patch('agent.tools.requests.get')
    def test_fetch_html_failure(self, mock_get):
        # Must raise a RequestException for the catch block to work
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        result = fetch_html("http://example.com")
        self.assertTrue(result.startswith("Error"))

    def test_clean_html(self):
        html = """
        <html>
            <nav>Menu</nav>
            <main>Content</main>
            <footer>Footer</footer>
            <div style="display:none">Hidden</div>
        </html>
        """
        cleaned = clean_html(html)
        self.assertNotIn("Menu", cleaned)
        self.assertNotIn("Footer", cleaned)
        self.assertNotIn("Hidden", cleaned)
        self.assertIn("Content", cleaned)

    def test_convert_to_markdown(self):
        html = "<h1>Title</h1><p>Paragraph</p>"
        md = convert_to_markdown(html)
        self.assertIn("# Title", md)
        self.assertIn("Paragraph", md)

    def test_extract_images(self):
        html = '<img src="image.png"><img src="/path/to/image.jpg">'
        base_url = "http://example.com"
        images = extract_images(html, base_url)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], "http://example.com/image.png")
        self.assertEqual(images[1], "http://example.com/path/to/image.jpg")

if __name__ == '__main__':
    unittest.main()
