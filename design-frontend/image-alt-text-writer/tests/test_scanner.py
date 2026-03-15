import pytest
import os
import sys
from unittest.mock import patch

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

def test_image_info_repr():
    info = ImageInfo("test.jpg", "alt", "ctx", "file.html", 10)
    assert repr(info) == "ImageInfo(src='test.jpg', alt='alt', filepath='file.html')"

def test_scan_file_missing_src(scanner, tmpdir):
    html_content = "<html><body><img><img alt='abc'></body></html>"
    test_file = tmpdir / "test.html"
    test_file.write_text(html_content, encoding='utf-8')
    results = scanner.scan_file(str(test_file))
    assert len(results) == 0

def test_scan_file_exception(scanner, tmpdir):
    test_file = tmpdir / "test.html"
    # don't write it, so reading it raises FileNotFoundError
    with patch('builtins.print') as mock_print:
        results = scanner.scan_file(str(test_file))
        assert len(results) == 0
        mock_print.assert_called_once()

def test_scan_directory(scanner, tmpdir):
    dir1 = tmpdir.mkdir("dir1")
    dir1.join("test1.html").write("<html><body><img src='1.jpg'></body></html>")
    dir2 = dir1.mkdir("dir2")
    dir2.join("test2.html").write("<html><body><img src='2.jpg'></body></html>")
    dir2.join("skip.txt").write("skip")
    
    # Recursive
    results = scanner.scan_directory(str(tmpdir), recursive=True)
    assert len(results) == 2
    
    # Non-recursive
    results = scanner.scan_directory(str(dir1), recursive=False)
    assert len(results) == 1

def test_scan_file_fallback_parser(scanner, tmpdir):
    html_content = "<html><body><img src='test.jpg'></body></html>"
    test_file = tmpdir / "test.html"
    test_file.write_text(html_content, encoding='utf-8')
def test_scan_file_fallback_parser(scanner, tmpdir):
    html_content = "<html><body><img src='test.jpg'></body></html>"
    test_file = tmpdir / "test.html"
    test_file.write_text(html_content, encoding='utf-8')
    
    def fake_bs(content, features):
        if features == 'lxml':
            raise ImportError("No module named lxml")
        from bs4 import BeautifulSoup as BS
        return BS(content, features)

    with patch('agent.scanner.BeautifulSoup', side_effect=fake_bs):
        results = scanner.scan_file(str(test_file))
        assert len(results) == 1
