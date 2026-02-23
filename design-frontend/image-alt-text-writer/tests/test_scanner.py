import pytest
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.scanner import Scanner, ImageInfo

@pytest.fixture
def scanner():
    return Scanner()

def test_scan_file_missing_alt(scanner, tmp_path):
    html_content = """
    <html>
        <body>
            <img src="test.jpg" alt="">
            <img src="test2.jpg">
            <img src="decorative.jpg" alt="" role="presentation">
        </body>
    </html>
    """
    test_file = tmp_path / "test.html"
    test_file.write_text(html_content, encoding='utf-8')

    results = scanner.scan_file(str(test_file))

    assert len(results) == 2
    assert results[0].src == "test.jpg"
    assert results[1].src == "test2.jpg"
