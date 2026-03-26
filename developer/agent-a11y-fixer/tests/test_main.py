"""Tests for A11Y Fixer Agent."""
import pytest
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import scan_html, generate_fix, generate_report, run, main, APP_NAME, APP_VERSION


# ── scan_html tests ──────────────────────────────────────────────────────────

class TestScanHtml:
    def test_clean_html(self):
        html = '<html><body><a href="#main">Skip</a><h1>Title</h1><img src="x" alt="photo"></body></html>'
        result = scan_html(html)
        assert result["total"] == 0
        assert result["issues"] == []

    def test_missing_alt(self):
        html = '<img src="photo.jpg">'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Missing Alt Text" in types

    def test_alt_present_no_issue(self):
        html = '<img src="x" alt="A photo">'
        result = scan_html(html)
        alt_issues = [i for i in result["issues"] if i["type"] == "Missing Alt Text"]
        assert len(alt_issues) == 0

    def test_missing_form_label(self):
        html = '<form><input type="text" id="name"></form>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Missing Form Label" in types

    def test_form_with_label(self):
        html = '<label for="name">Name</label><input type="text" id="name">'
        result = scan_html(html)
        label_issues = [i for i in result["issues"] if i["type"] == "Missing Form Label"]
        assert len(label_issues) == 0

    def test_form_with_aria_label(self):
        html = '<input type="text" aria-label="Search">'
        result = scan_html(html)
        label_issues = [i for i in result["issues"] if i["type"] == "Missing Form Label"]
        assert len(label_issues) == 0

    def test_skip_hidden_submit_button_inputs(self):
        html = '<input type="submit"><input type="button"><input type="hidden">'
        result = scan_html(html)
        label_issues = [i for i in result["issues"] if i["type"] == "Missing Form Label"]
        assert len(label_issues) == 0

    def test_textarea_missing_label(self):
        html = '<textarea id="bio"></textarea>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Missing Form Label" in types

    def test_select_missing_label(self):
        html = '<select id="country"><option>US</option></select>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Missing Form Label" in types

    def test_missing_skip_link(self):
        html = '<html><body><a href="/about">About</a><h1>Title</h1></body></html>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Missing Skip Link" in types

    def test_skip_link_present(self):
        html = '<a href="#main">Skip</a>'
        result = scan_html(html)
        skip_issues = [i for i in result["issues"] if i["type"] == "Missing Skip Link"]
        assert len(skip_issues) == 0

    def test_empty_link(self):
        html = '<a href="/page">   </a>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Empty Link" in types

    def test_empty_link_with_aria(self):
        html = '<a href="/page" aria-label="Go to page"> </a>'
        result = scan_html(html)
        empty_issues = [i for i in result["issues"] if i["type"] == "Empty Link"]
        assert len(empty_issues) == 0

    def test_heading_hierarchy_skip(self):
        html = '<h1>Title</h1><h3>Sub</h3>'
        result = scan_html(html)
        types = [i["type"] for i in result["issues"]]
        assert "Heading Hierarchy Skip" in types

    def test_heading_hierarchy_ok(self):
        html = '<h1>Title</h1><h2>Sub</h2><h3>Detail</h3>'
        result = scan_html(html)
        hierarchy_issues = [i for i in result["issues"] if i["type"] == "Heading Hierarchy Skip"]
        assert len(hierarchy_issues) == 0

    def test_multiple_issues(self):
        html = '<html><body><a href="/x">Link</a><img src="x"><input type="text"><h1>A</h1><h4>B</h4></body></html>'
        result = scan_html(html)
        assert result["total"] >= 3


# ── generate_fix tests ───────────────────────────────────────────────────────

class TestGenerateFix:
    def test_adds_skip_link(self):
        html = "<body><h1>Title</h1></body>"
        issues = [{"type": "Missing Skip Link"}]
        fixed = generate_fix(html, issues)
        assert 'href="#main"' in fixed
        assert "skip-link" in fixed

    def test_adds_alt_to_images(self):
        html = '<img src="photo.jpg">'
        issues = [{"type": "Missing Alt Text"}]
        fixed = generate_fix(html, issues)
        assert 'alt=""' in fixed

    def test_preserves_existing_alt(self):
        html = '<img src="x" alt="Photo">'
        issues = []
        fixed = generate_fix(html, issues)
        assert 'alt="Photo"' in fixed

    def test_no_changes_when_clean(self):
        html = '<body><a href="#main">Skip</a><img src="x" alt="ok"></body>'
        fixed = generate_fix(html, [])
        assert fixed == html


# ── generate_report tests ────────────────────────────────────────────────────

class TestGenerateReport:
    def test_json_format(self):
        result = {"issues": [{"type": "Test", "severity": "critical", "element": "<img>", "description": "Desc", "recommendation": "Fix"}], "total": 1}
        report = generate_report(result, "json")
        parsed = json.loads(report)
        assert parsed["total"] == 1

    def test_text_format(self):
        result = {"issues": [{"type": "Test", "severity": "critical", "element": "<img>", "description": "Desc", "recommendation": "Fix"}], "total": 1}
        report = generate_report(result, "text")
        assert "Test" in report
        assert "critical" in report

    def test_no_issues(self):
        result = {"issues": [], "total": 0}
        report = generate_report(result)
        assert "No accessibility issues" in report


# ── run() tests ──────────────────────────────────────────────────────────────

class TestRun:
    def test_empty_input(self):
        result = run("")
        assert "Please provide HTML" in result

    def test_whitespace_input(self):
        result = run("   ")
        assert "Please provide HTML" in result

    def test_valid_html(self):
        result = run('<html><body><a href="#main">Skip</a><h1>Hi</h1></body></html>')
        assert "No accessibility issues" in result

    def test_html_with_issues(self):
        result = run('<img src="x">')
        assert "Missing Alt Text" in result


# ── main() CLI tests ─────────────────────────────────────────────────────────

class TestMain:
    def test_no_file(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.argv", ["main.py"])
        main()
        out = capsys.readouterr().out
        assert "Please provide HTML" in out

    def test_file_not_found(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.argv", ["main.py", "/nonexistent/file.html"])
        with pytest.raises(SystemExit):
            main()

    def test_scan_file(self, capsys, monkeypatch, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text('<html><body><a href="#main">Skip</a><h1>Hi</h1></body></html>')
        monkeypatch.setattr("sys.argv", ["main.py", str(html_file)])
        main()
        out = capsys.readouterr().out
        assert "No accessibility issues" in out

    def test_scan_with_json_format(self, capsys, monkeypatch, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text('<img src="x">')
        monkeypatch.setattr("sys.argv", ["main.py", str(html_file), "--format", "json"])
        main()
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["total"] >= 1

    def test_scan_with_output_file(self, capsys, monkeypatch, tmp_path):
        html_file = tmp_path / "test.html"
        html_file.write_text('<img src="x">')
        out_file = tmp_path / "report.txt"
        monkeypatch.setattr("sys.argv", ["main.py", str(html_file), "--out", str(out_file)])
        main()
        assert out_file.exists()
        assert "Missing Alt Text" in out_file.read_text()

    def test_fix_mode(self, capsys, monkeypatch, tmp_path):
        html_file = tmp_path / "page.html"
        html_file.write_text('<body><img src="x"></body>')
        monkeypatch.setattr("sys.argv", ["main.py", str(html_file), "--fix"])
        main()
        fixed_path = tmp_path / "page_fixed.html"
        assert fixed_path.exists()
        assert 'alt=""' in fixed_path.read_text()


# ── Config test ──────────────────────────────────────────────────────────────

class TestConfig:
    def test_app_metadata(self):
        assert APP_NAME == "a11y-fixer"
        assert APP_VERSION == "1.0.0"

    def test_config_module(self):
        from config import APP_NAME as cfg_name, APP_VERSION as cfg_ver, DESCRIPTION, COMMANDS, SEVERITY_LEVELS
        assert cfg_name == "a11y-fixer"
        assert cfg_ver == "1.0.0"
        assert "Scans HTML" in DESCRIPTION
        assert "scan" in COMMANDS
        assert "critical" in SEVERITY_LEVELS
