"""Tests for SEO Auditor agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "SEO Auditor" in result


class TestAuditHtml:
    """Test the audit_html function via capsys since it prints directly."""

    def test_good_html(self, capsys):
        from main import audit_html
        html = '<html><head><title>Great Page Title</title><meta name="description" content="A proper meta description that is long enough to be meaningful for search engines."></head><body><h1>Main Heading</h1></body></html>'
        audit_html(html, "test")
        output = capsys.readouterr().out
        assert "✅" in output

    def test_missing_title(self, capsys):
        from main import audit_html
        html = "<html><body><h1>Hello</h1></body></html>"
        audit_html(html, "test")
        output = capsys.readouterr().out
        assert "Missing" in output and "title" in output.lower()

    def test_missing_meta_description(self, capsys):
        from main import audit_html
        html = "<html><head><title>Page</title></head><body><h1>Hello</h1></body></html>"
        audit_html(html, "test")
        output = capsys.readouterr().out
        assert "meta description" in output.lower()

    def test_multiple_h1(self, capsys):
        from main import audit_html
        html = "<html><head><title>Page Title Here</title></head><body><h1>First</h1><h1>Second</h1></body></html>"
        audit_html(html, "test")
        output = capsys.readouterr().out
        assert "Multiple" in output

    def test_missing_alt_text(self, capsys):
        from main import audit_html
        html = '<html><head><title>Page Title Here</title></head><body><h1>Hi</h1><img src="pic.jpg"></body></html>'
        audit_html(html, "test")
        output = capsys.readouterr().out
        assert "alt text" in output.lower()
