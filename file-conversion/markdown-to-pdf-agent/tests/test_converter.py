import pytest
from unittest.mock import patch, MagicMock
from agent.converter import PDFConverter

def test_convert_success(tmp_path):
    converter = PDFConverter()
    md = "# Hello\n\nThis is a test."
    theme = {
        "h1": {"font": "Helvetica", "size": 24, "style": "B", "color": [44, 62, 80], "margin_top": 10},
        "p": {"font": "Helvetica", "size": 11, "style": "", "color": [51, 51, 51], "line_height": 6},
        "page": {"margins": 10}
    }
    out = tmp_path / "out.pdf"

    # Mock ThemeFPDF which is used inside convert
    with patch("agent.converter.ThemeFPDF") as MockThemeFPDF:
        mock_pdf = MockThemeFPDF.return_value
        res = converter.convert(md, theme, str(out))
        assert res is True
        mock_pdf.output.assert_called_with(str(out))

        # Verify calls
        mock_pdf.add_page.assert_called()
        # Should set font for H1 (Helvetica, B, 24)
        mock_pdf.set_font.assert_any_call("Helvetica", "B", 24)

def test_convert_failure(tmp_path):
    converter = PDFConverter()
    md = "# Hello"
    theme = {}
    out = tmp_path / "out.pdf"

    with patch("agent.converter.ThemeFPDF") as MockThemeFPDF:
        mock_pdf = MockThemeFPDF.return_value
        mock_pdf.output.side_effect = Exception("Write Error")
        res = converter.convert(md, theme, str(out))
        assert res is False
