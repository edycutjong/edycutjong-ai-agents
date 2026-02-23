import pytest
from unittest.mock import MagicMock, patch, mock_open
from agent.exporter import SOPExporter
import os

@pytest.fixture
def mock_open_file():
    with patch("builtins.open", mock_open()) as mock_file:
        yield mock_file

@pytest.fixture
def mock_reportlab():
    with patch("agent.exporter.SimpleDocTemplate") as MockDocTemplate:
        yield MockDocTemplate

def test_save_markdown(mock_open_file):
    exporter = SOPExporter(output_dir="test_output")
    # Patch os.path.exists and os.makedirs to avoid creating actual dirs
    with patch("os.path.exists", return_value=True), \
         patch("os.makedirs"):
        filepath = exporter.save_markdown("Test Content", filename="test.md")

        assert filepath == os.path.join("test_output", "test.md")
        mock_open_file.assert_called_with(filepath, "w", encoding="utf-8")
        mock_open_file().write.assert_called_with("Test Content")

def test_save_pdf(mock_reportlab):
    exporter = SOPExporter(output_dir="test_output")
    # Patch os.path.exists
    with patch("os.path.exists", return_value=True):
        filepath = exporter.save_pdf("# Test Content", filename="test.pdf")

        assert filepath == os.path.join("test_output", "test.pdf")
        mock_reportlab.assert_called()
        # Verify build was called on the doc template instance
        mock_reportlab.return_value.build.assert_called()

def test_save_pdf_error(mock_reportlab):
    exporter = SOPExporter(output_dir="test_output")
    mock_reportlab.return_value.build.side_effect = Exception("PDF Error")

    with patch("os.path.exists", return_value=True):
        filepath = exporter.save_pdf("Content", "fail.pdf")
        # Should return None on error
        assert filepath is None

def test_save_pdf_complex_content(mock_reportlab):
    exporter = SOPExporter(output_dir="test_output")
    content = """
# Title
## H2
### H3
- Item 1
* Item 2
1. Enum
Normal text
```mermaid
graph TD
```
```
code block
```
    """
    with patch("os.path.exists", return_value=True):
        filepath = exporter.save_pdf(content, filename="complex.pdf")
        assert filepath is not None
        mock_reportlab.assert_called()
