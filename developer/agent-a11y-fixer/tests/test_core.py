import os
import pytest
from agent.core import A11yFixer
from agent.utils import calculate_luminance, contrast_ratio, analyze_contrast

# Dummy test matching requirements
def test_luminance_calculation():
    # White luminance is 1.0, black is 0.0
    assert abs(calculate_luminance("#FFFFFF") - 1.0) < 0.01
    assert abs(calculate_luminance("#000000") - 0.0) < 0.01

def test_contrast_ratio():
    # White vs Black should be 21:1
    assert abs(contrast_ratio("#FFFFFF", "#000000") - 21.0) < 0.1

def test_analyze_contrast():
    result = analyze_contrast("#FFFFFF", "#000000")
    assert result["passes_aa"] is True
    assert result["passes_aaa"] is True

    result2 = analyze_contrast("#FFFFFF", "#EEEEEE")
    assert result2["passes_aa"] is False

def test_scan_html_finds_missing_alt():
    fixer = A11yFixer(api_key="DUMMY_KEY_FOR_TESTS")
    bad_html = "<html><body><img src='test.png'></body></html>"
    result = fixer.scan_html(bad_html)
    assert len(result["issues"]) > 0
    assert result["issues"][0]["type"] == "Missing Alt Text"

def test_scan_html_finds_missing_label():
    fixer = A11yFixer(api_key="DUMMY_KEY_FOR_TESTS")
    bad_html = "<html><body><input type='text' id='name'></body></html>"
    result = fixer.scan_html(bad_html)
    assert any(issue["type"] == "Missing Form Label" for issue in result["issues"])

def test_scan_html_clean():
    fixer = A11yFixer(api_key="DUMMY_KEY_FOR_TESTS")
    good_html = "<html><body><a href='#main'>Skip</a><img src='t.png' alt='test'><label for='n'>Name</label><input type='text' id='n'></body></html>"
    result = fixer.scan_html(good_html)
    assert len(result["issues"]) == 0
