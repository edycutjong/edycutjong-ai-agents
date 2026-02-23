from unittest.mock import MagicMock, patch
import sys
import os

# Ensure mocks are in place if imported directly
if 'fpdf' not in sys.modules:
    sys.modules['fpdf'] = MagicMock()

from agent.tools import save_to_markdown, save_to_pdf, FPDF

def test_save_to_markdown(tmp_path):
    content = "# Test"
    filename = tmp_path / "test.md"
    result = save_to_markdown(content, str(filename))

    assert result == str(filename)
    with open(filename, 'r', encoding='utf-8') as f:
        assert f.read() == content

def test_save_to_pdf_calls_fpdf():
    # Since FPDF is mocked via sys.modules or existing mock
    # We verify that save_to_pdf instantiates PDF (subclass of FPDF) and calls output.

    content = "Test PDF Content"
    filename = "test_output.pdf"

    # We need to patch PDF inside agent.tools because that's the class being used
    with patch('agent.tools.PDF') as MockPDF:
        instance = MockPDF.return_value

        result = save_to_pdf(content, filename)

        MockPDF.assert_called_once()
        instance.add_page.assert_called_once()
        instance.set_font.assert_called_with("Arial", size=12)
        instance.multi_cell.assert_called_with(0, 10, content)
        instance.output.assert_called_with(filename)
        assert result == filename
