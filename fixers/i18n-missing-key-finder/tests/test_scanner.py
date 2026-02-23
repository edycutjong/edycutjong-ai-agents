import sys
import os
import pytest

# Add parent directory to path to allow importing 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.scanner import Scanner

# Create a temporary directory structure for testing
@pytest.fixture
def scanner_test_dir(tmp_path):
    d = tmp_path / "src"
    d.mkdir()

    # Python file
    p = d / "app.py"
    # Create the file with explicit UTF-8 encoding
    with open(p, 'w', encoding='utf-8') as f:
        f.write("print(t('hello_world'))\nprint(i18n.t('nested.key'))")

    # JS file
    j = d / "component.js"
    with open(j, 'w', encoding='utf-8') as f:
        f.write("const msg = t(\"js_key\");\nconst other = i18n.t('another_key');")

    # HTML file
    h = d / "index.html"
    with open(h, 'w', encoding='utf-8') as f:
        f.write("<div>{{ 'liquid_key' | t }}</div>")

    return d

def test_scanner_finds_keys(scanner_test_dir):
    scanner = Scanner()
    keys = scanner.scan_directory(str(scanner_test_dir))

    expected_keys = {
        'hello_world',
        'nested.key',
        'js_key',
        'another_key',
        'liquid_key'
    }

    assert keys == expected_keys

def test_scanner_finds_spaced_keys(tmp_path):
    # Test for spaces around keys
    f = tmp_path / "spaced.js"
    with open(f, 'w', encoding='utf-8') as file:
        file.write("t( 'spaced_key' ); i18n.t(  \"double_spaced\"  );")

    scanner = Scanner()
    keys = scanner.scan_file(str(f))

    assert 'spaced_key' in keys
    assert 'double_spaced' in keys

def test_scanner_ignores_dirs(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    p = src / "valid.py"
    with open(p, 'w', encoding='utf-8') as f:
        f.write("t('valid_key')")

    ignored = src / "node_modules"
    ignored.mkdir()
    b = ignored / "bad.js"
    with open(b, 'w', encoding='utf-8') as f:
        f.write("t('ignored_key')")

    scanner = Scanner()
    keys = scanner.scan_directory(str(src))

    assert 'valid_key' in keys
    assert 'ignored_key' not in keys

def test_scanner_custom_patterns(tmp_path):
    f = tmp_path / "custom.txt"
    with open(f, 'w', encoding='utf-8') as file:
        file.write("custom_func('my_key')")

    scanner = Scanner(patterns=[r"custom_func\('(.+?)'\)"], extensions={'.txt'})
    keys = scanner.scan_file(str(f))

    assert keys == {'my_key'}
