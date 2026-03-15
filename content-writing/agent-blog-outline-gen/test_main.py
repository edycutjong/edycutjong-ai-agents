"""Tests for Blog Outline Generator agent."""
import pytest
from main import run, generate_outline


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Blog Outline Generator" in result


class TestGenerateOutline:
    def test_generates_outline_with_topic(self):
        outline = generate_outline("Python Async")
        assert "Python Async" in outline
        assert "Introduction" in outline
        assert "Conclusion" in outline

    def test_includes_audience(self):
        outline = generate_outline("Testing", audience="QA engineers")
        assert "QA engineers" in outline

    def test_custom_word_count(self):
        outline = generate_outline("Topic", length=3000)
        assert "3000" in outline

    def test_includes_seo_elements(self):
        outline = generate_outline("React Hooks")
        assert "meta description" in outline.lower() or "SEO" in outline
        assert "tags" in outline.lower()

    def test_has_multiple_sections(self):
        outline = generate_outline("GraphQL")
        assert outline.count("## ") >= 5
