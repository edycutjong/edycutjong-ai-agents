import sys
import os
import pytest

# Add parent directory to path to allow importing 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.analyzer import Analyzer

def test_analyze_simple():
    # Source code has keys: 'key1', 'key2'
    source_keys = {'key1', 'key2'}

    # Locales have:
    # en: 'key1' (missing 'key2')
    # fr: 'key1', 'key2', 'key3' (unused 'key3')
    locales = {
        'en': {'key1': 'val1'},
        'fr': {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
    }

    analyzer = Analyzer(source_keys, locales)
    result = analyzer.analyze()

    # Check EN
    assert 'key2' in result.missing_keys['en']
    assert len(result.unused_keys['en']) == 0

    # Check FR
    assert len(result.missing_keys['fr']) == 0
    assert 'key3' in result.unused_keys['fr']

def test_analyze_empty():
    source_keys = set()
    locales = {'en': {'key1': 'val1'}}

    analyzer = Analyzer(source_keys, locales)
    result = analyzer.analyze()

    assert len(result.missing_keys['en']) == 0
    assert 'key1' in result.unused_keys['en']
