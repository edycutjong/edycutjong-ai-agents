"""Tests for HTML to Markdown Converter."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import html_to_markdown, strip_tags, extract_links, extract_images, format_result_markdown

def test_heading(): r = html_to_markdown("<h1>Title</h1>"); assert r.markdown == "# Title"
def test_h2(): r = html_to_markdown("<h2>Sub</h2>"); assert r.markdown == "## Sub"
def test_bold(): r = html_to_markdown("<strong>bold</strong>"); assert r.markdown == "**bold**"
def test_italic(): r = html_to_markdown("<em>italic</em>"); assert r.markdown == "*italic*"
def test_code(): r = html_to_markdown("<code>x</code>"); assert r.markdown == "`x`"
def test_link(): r = html_to_markdown('<a href="https://x.com">link</a>'); assert "[link](https://x.com)" in r.markdown
def test_image(): r = html_to_markdown('<img src="img.png" alt="pic">'); assert "![pic](img.png)" in r.markdown
def test_list(): r = html_to_markdown("<ul><li>one</li><li>two</li></ul>"); assert "- one" in r.markdown
def test_paragraph(): r = html_to_markdown("<p>Hello</p>"); assert "Hello" in r.markdown
def test_br(): r = html_to_markdown("a<br>b"); assert "\n" in r.markdown
def test_hr(): r = html_to_markdown("<hr>"); assert "---" in r.markdown
def test_blockquote(): r = html_to_markdown("<blockquote>quote</blockquote>"); assert "> quote" in r.markdown
def test_strip(): assert strip_tags("<b>hello</b>") == "hello"
def test_extract_links(): links = extract_links('<a href="x.com">X</a>'); assert len(links) == 1
def test_extract_images(): imgs = extract_images('<img src="a.png">'); assert "a.png" in imgs
def test_empty(): r = html_to_markdown(""); assert r.markdown == ""
def test_plain(): r = html_to_markdown("just text"); assert r.markdown == "just text"
def test_format(): md = format_result_markdown(html_to_markdown("<h1>Hi</h1>")); assert "HTML→MD" in md
def test_to_dict(): d = html_to_markdown("<h1>Hi</h1>").to_dict(); assert "md_len" in d
