"""Tests for HTML to Markdown converter."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import html_to_markdown, strip_tags, convert_with_stats

def test_headers():
    assert "# Hello" in html_to_markdown("<h1>Hello</h1>")
    assert "## Sub" in html_to_markdown("<h2>Sub</h2>")

def test_bold(): assert "**bold**" in html_to_markdown("<strong>bold</strong>")
def test_italic(): assert "*italic*" in html_to_markdown("<em>italic</em>")
def test_code(): assert "`code`" in html_to_markdown("<code>code</code>")

def test_link():
    md = html_to_markdown('<a href="https://example.com">click</a>')
    assert "[click](https://example.com)" in md

def test_image():
    md = html_to_markdown('<img src="img.png" alt="photo"/>')
    assert "![photo](img.png)" in md

def test_list():
    md = html_to_markdown("<ul><li>one</li><li>two</li></ul>")
    assert "- one" in md and "- two" in md

def test_paragraph():
    md = html_to_markdown("<p>Hello world</p>")
    assert "Hello world" in md

def test_br():
    md = html_to_markdown("line1<br/>line2")
    assert "line1" in md and "line2" in md

def test_hr():
    md = html_to_markdown("<hr/>")
    assert "---" in md

def test_strip_scripts():
    md = html_to_markdown('<script>alert("x")</script><p>safe</p>')
    assert "alert" not in md and "safe" in md

def test_entities():
    md = html_to_markdown("&amp; &lt; &gt;")
    assert "& < >" in md

def test_strip_tags():
    assert strip_tags("<p>hello</p>") == "hello"

def test_blockquote():
    md = html_to_markdown("<blockquote>quoted</blockquote>")
    assert "> quoted" in md

def test_pre_code():
    md = html_to_markdown("<pre><code>x = 1</code></pre>")
    assert "```" in md and "x = 1" in md

def test_stats():
    md, stats = convert_with_stats("<h1>Hello</h1><p>World</p>")
    assert stats.input_chars > stats.output_chars
    assert stats.tags_removed >= 4
    assert stats.reduction_pct > 0

def test_empty():
    assert html_to_markdown("") == ""

def test_nested():
    md = html_to_markdown("<p><strong>bold <em>italic</em></strong></p>")
    assert "**bold *italic***" in md
