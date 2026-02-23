"""Tests for Accessibility Auditor."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.auditor import audit_html, format_result_markdown

GOOD_HTML = '<html lang="en"><head><title>Test</title></head><body><h1>Hello</h1><img src="x.png" alt="photo"><a href="/">Home</a></body></html>'
BAD_HTML = '<html><head></head><body><h3>Skip</h3><img src="x.png"><a href="/"></a><input id="name"></body></html>'

def test_good_html():
    r = audit_html(GOOD_HTML)
    assert r.errors == 0

def test_img_no_alt():
    r = audit_html('<img src="test.png">')
    assert any(i.rule == "img-alt" for i in r.issues)

def test_img_with_alt():
    r = audit_html('<img src="test.png" alt="description">')
    assert not any(i.rule == "img-alt" for i in r.issues)

def test_empty_link():
    r = audit_html('<a href="/page"></a>')
    assert any(i.rule == "link-text" for i in r.issues)

def test_link_with_text():
    r = audit_html('<a href="/page">Click</a>')
    assert not any(i.rule == "link-text" for i in r.issues)

def test_missing_lang():
    r = audit_html('<html><head><title>T</title></head></html>')
    assert any(i.rule == "html-lang" for i in r.issues)

def test_has_lang():
    r = audit_html('<html lang="en"><head><title>T</title></head></html>')
    assert not any(i.rule == "html-lang" for i in r.issues)

def test_missing_title():
    r = audit_html('<html lang="en"><head></head></html>')
    assert any(i.rule == "page-title" for i in r.issues)

def test_heading_skip():
    r = audit_html('<h1>Title</h1><h3>Sub</h3>')
    assert any(i.rule == "heading-order" for i in r.issues)

def test_heading_order_ok():
    r = audit_html('<h1>A</h1><h2>B</h2><h3>C</h3>')
    assert not any(i.rule == "heading-order" and "skipped" in i.message for i in r.issues)

def test_small_text():
    r = audit_html('<span style="font-size:8px">tiny</span>')
    assert any(i.rule == "text-size" for i in r.issues)

def test_score_perfect():
    r = audit_html(GOOD_HTML)
    assert r.score >= 90

def test_score_bad():
    r = audit_html(BAD_HTML)
    assert r.score < 80

def test_format_good():
    r = audit_html(GOOD_HTML)
    md = format_result_markdown(r)
    assert "✅" in md

def test_format_bad():
    r = audit_html(BAD_HTML)
    md = format_result_markdown(r)
    assert "Errors" in md or "error" in md.lower()

def test_to_dict():
    r = audit_html(BAD_HTML)
    d = r.to_dict()
    assert "score" in d and "errors" in d
