import os
import unittest
from unittest.mock import MagicMock, patch
from agent.pdf_parser import extract_text_from_pdf

class TestPdfParser(unittest.TestCase):

    @patch('agent.pdf_parser.PdfReader')
    def test_extract_text_success(self, MockPdfReader):
        # Setup mock
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page content"

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        MockPdfReader.return_value = mock_reader

        text = extract_text_from_pdf("dummy.pdf")
        self.assertEqual(text, "Page content")

    @patch('agent.pdf_parser.PdfReader')
    def test_extract_text_empty(self, MockPdfReader):
        # Setup mock with empty page
        mock_page = MagicMock()
        mock_page.extract_text.return_value = ""

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        MockPdfReader.return_value = mock_reader

        text = extract_text_from_pdf("dummy.pdf")
        self.assertEqual(text, "")

    @patch('agent.pdf_parser.PdfReader')
    def test_extract_text_failure(self, MockPdfReader):
        MockPdfReader.side_effect = Exception("File not found")

        text = extract_text_from_pdf("nonexistent.pdf")
        self.assertIsNone(text)

if __name__ == '__main__':
    unittest.main()
