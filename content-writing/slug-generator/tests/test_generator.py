"""Tests for Slug Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import slugify, batch_slugify, is_valid_slug, format_result_markdown

def test_basic(): assert slugify("Hello World").slug == "hello-world"
def test_special(): assert slugify("Hello, World!").slug == "hello-world"
def test_spaces(): assert slugify("  multiple   spaces  ").slug == "multiple-spaces"
def test_uppercase(): assert slugify("UPPERCASE TEXT").slug == "uppercase-text"
def test_no_lower(): assert slugify("Hello", lowercase=False).slug == "Hello"
def test_separator(): assert slugify("hello world", separator="_").slug == "hello_world"
def test_max_length(): r = slugify("a very long title here", max_length=10); assert len(r.slug) <= 10 and r.truncated
def test_no_truncate(): r = slugify("short", max_length=20); assert not r.truncated
def test_umlaut(): assert "ue" in slugify("über cool").slug
def test_unicode(): r = slugify("café résumé"); assert r.slug and is_valid_slug(r.slug)
def test_valid_slug(): assert is_valid_slug("hello-world")
def test_invalid_slug(): assert not is_valid_slug("Hello World!")
def test_empty(): assert slugify("").slug == ""
def test_numbers(): assert slugify("test 123").slug == "test-123"
def test_batch(): results = batch_slugify(["Hello", "World"]); assert len(results) == 2
def test_batch_dedup(): results = batch_slugify(["Hello", "Hello"]); assert results[0].slug != results[1].slug
def test_format(): md = format_result_markdown(slugify("test")); assert "Slug Generator" in md
def test_to_dict(): d = slugify("test").to_dict(); assert "slug" in d
