import pytest
import os
import sys

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.parser import parse_css_file, CSSRule
from tools.scanner import scan_file
from tools.detector import find_unused_rules, audit_media_queries
from tools.cleaner import purge_css, minify_css

@pytest.fixture
def sample_css_path(tmp_path):
    css_content = """
    body { margin: 0; }
    .used { color: blue; }
    .unused { color: red; }
    @media (max-width: 600px) {
        .used-mobile { display: block; }
        .unused-mobile { display: none; }
    }
    """
    path = tmp_path / "style.css"
    path.write_text(css_content, encoding='utf-8')
    return str(path)

@pytest.fixture
def sample_html_path(tmp_path):
    html_content = """
    <html>
    <body class="used">
        <div class="used-mobile"></div>
    </body>
    </html>
    """
    path = tmp_path / "index.html"
    path.write_text(html_content, encoding='utf-8')
    return str(path)

def test_parser(sample_css_path):
    rules = parse_css_file(sample_css_path)
    # body, .used, .unused, .used-mobile, .unused-mobile -> 5 rules
    assert len(rules) == 5
    selectors = [r.selectors[0] for r in rules]
    assert 'body' in selectors
    assert '.used' in selectors
    assert '.unused' in selectors
    assert '.used-mobile' in selectors

def test_scanner(sample_html_path):
    selectors = scan_file(sample_html_path)
    assert 'body' in selectors
    assert '.used' in selectors
    assert '.used-mobile' in selectors
    assert '.unused' not in selectors

def test_detector(sample_css_path, sample_html_path):
    rules = parse_css_file(sample_css_path)
    used_selectors = scan_file(sample_html_path)

    unused = find_unused_rules(rules, used_selectors)

    # unused should contain .unused and .unused-mobile
    unused_selectors = [r.selectors[0] for r in unused]
    assert '.unused' in unused_selectors
    assert '.unused-mobile' in unused_selectors
    assert '.used' not in unused_selectors
    assert 'body' not in unused_selectors

def test_media_audit(sample_css_path):
    rules = parse_css_file(sample_css_path)
    stats = audit_media_queries(rules)

    # 3 rules with no media (body, .used, .unused)
    # 2 rules with media (.used-mobile, .unused-mobile)
    assert stats['No Media Query'] == 3
    assert stats['(max-width: 600px)'] == 2

def test_cleaner(sample_css_path, tmp_path):
    rules = parse_css_file(sample_css_path)
    # Simulate unused list
    unused = [r for r in rules if '.unused' in r.selectors[0]]

    output_path = tmp_path / "clean.css"
    purge_css(sample_css_path, unused, str(output_path))

    cleaned = output_path.read_text(encoding='utf-8')
    assert '.unused' not in cleaned
    assert '.used' in cleaned
    assert '.used-mobile' in cleaned

def test_minify(sample_css_path, tmp_path):
    original = open(sample_css_path).read()
    minified = minify_css(original)

    assert len(minified) < len(original)
    assert '{' in minified
    # Basic check
