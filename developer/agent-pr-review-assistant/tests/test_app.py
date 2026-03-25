"""Tests for agent-pr-review-assistant."""

import pytest
from unittest.mock import patch, MagicMock
from app import parse_pr_url, analyse_file, build_review, fetch_pr_info, fetch_pr_files


# ── parse_pr_url ─────────────────────────────────────────────


class TestParsePrUrl:
    def test_valid_url(self):
        result = parse_pr_url("https://github.com/octocat/hello-world/pull/42")
        assert result == {"owner": "octocat", "repo": "hello-world", "number": 42}

    def test_trailing_whitespace(self):
        result = parse_pr_url("  https://github.com/a/b/pull/1  ")
        assert result["number"] == 1

    def test_invalid_url(self):
        assert parse_pr_url("https://github.com/a/b") is None

    def test_not_a_url(self):
        assert parse_pr_url("not a url") is None

    def test_empty(self):
        assert parse_pr_url("") is None


# ── analyse_file ─────────────────────────────────────────────


class TestAnalyseFile:
    def _file(self, filename="main.py", patch="", additions=10):
        return {"filename": filename, "patch": patch, "additions": additions}

    def test_large_file(self):
        findings = analyse_file(self._file(additions=500))
        assert any(f["title"] == "Large change" for f in findings)

    def test_todo_detection(self):
        findings = analyse_file(self._file(patch="+# TODO: fix later"))
        assert any("TODO" in f["title"] for f in findings)

    def test_fixme_detection(self):
        findings = analyse_file(self._file(patch="+# FIXME: broken"))
        assert any("TODO" in f["title"] for f in findings)

    def test_hardcoded_password(self):
        findings = analyse_file(self._file(patch="+password = 'secret123'"))
        assert any(f["severity"] == "critical" for f in findings)

    def test_hardcoded_api_key(self):
        findings = analyse_file(self._file(patch="+api_key = 'abc123'"))
        assert any(f["severity"] == "critical" for f in findings)

    def test_eval_usage(self):
        findings = analyse_file(self._file(patch="+eval(user_input)"))
        assert any("eval" in f["title"] for f in findings)

    def test_missing_test_file(self):
        findings = analyse_file(self._file(filename="utils.py"))
        assert any("test" in f["title"].lower() for f in findings)

    def test_test_files_skipped(self):
        findings = analyse_file(self._file(filename="test_utils.py", patch=""))
        assert not any("test" in f["title"].lower() for f in findings)

    def test_hardcoded_ip(self):
        findings = analyse_file(self._file(patch="+host = '192.168.1.1'"))
        assert any("IP" in f["title"] for f in findings)

    def test_clean_file(self):
        findings = analyse_file(self._file(filename="test_main.py", patch="+x = 1"))
        assert len(findings) == 0


# ── build_review ─────────────────────────────────────────────


class TestBuildReview:
    def _pr(self):
        return {"number": 1, "title": "Fix bug", "user": {"login": "dev"}}

    def test_no_findings(self):
        findings, md = build_review(self._pr(), [])
        assert len(findings) == 0
        assert "No issues found" in md

    def test_with_findings(self):
        files = [{"filename": "main.py", "patch": "+password = 'abc'", "additions": 5}]
        findings, md = build_review(self._pr(), files)
        assert len(findings) > 0
        assert "CRITICAL" in md

    def test_markdown_contains_pr_title(self):
        _, md = build_review(self._pr(), [])
        assert "Fix bug" in md


# ── fetch functions (mocked) ─────────────────────────────────


class TestFetch:
    @patch("app.requests.get")
    def test_fetch_pr_info(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"title": "Test PR"}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_pr_info("owner", "repo", 1)
        assert result["title"] == "Test PR"

    @patch("app.requests.get")
    def test_fetch_pr_files(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"filename": "a.py"}]
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        result = fetch_pr_files("owner", "repo", 1)
        assert len(result) == 1

    @patch("app.requests.get")
    def test_fetch_with_token(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        fetch_pr_info("o", "r", 1, token="ghp_test")
        call_args = mock_get.call_args
        assert "Authorization" in call_args.kwargs.get("headers", call_args[1].get("headers", {}))

    @patch("app.requests.get")
    def test_fetch_pr_files_with_token(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        fetch_pr_files("o", "r", 1, token="ghp_test")
        call_args = mock_get.call_args
        assert "Authorization" in call_args.kwargs.get("headers", call_args[1].get("headers", {}))

from app import _badge
class TestBadge:
    def test_badge(self):
        assert 'class="badge-info"' in _badge("info", "test")

from streamlit.testing.v1 import AppTest

class TestUI:
    def test_empty_pr_url(self):
        at = AppTest.from_file("app.py").run()
        at.text_input(key="pr_url").set_value("")
        at.button(key="run_btn").click().run()
        assert "Please enter a PR URL." in at.error[0].value

    def test_invalid_pr_url(self):
        at = AppTest.from_file("app.py").run()
        at.text_input(key="pr_url").set_value("invalid url")
        at.button(key="run_btn").click().run()
        assert "Invalid GitHub PR URL" in at.error[0].value

    @patch("app.requests.get")
    def test_api_error(self, mock_get):
        import requests
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.reason = "Not Found"
        mock_err = requests.HTTPError(response=mock_resp)
        mock_get.side_effect = mock_err

        at = AppTest.from_file("app.py").run()
        at.text_input(key="pr_url").set_value("https://github.com/abc/def/pull/1")
        at.button(key="run_btn").click().run()
        assert "GitHub API error: 404" in at.error[0].value

    @patch("app.requests.get")
    def test_no_findings(self, mock_get):
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {"number": 1, "title": "Test PR", "user": {"login": "dev"}}
        mock_resp1.raise_for_status = MagicMock()
        
        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = [{"filename": "test_main.py", "patch": "+x = 1", "additions": 1}]
        mock_resp2.raise_for_status = MagicMock()
        
        mock_get.side_effect = [mock_resp1, mock_resp2]
        
        at = AppTest.from_file("app.py").run()
        at.text_input(key="pr_url").set_value("https://github.com/abc/def/pull/1")
        at.button(key="run_btn").click().run()
        assert "✅ No issues found" in at.success[0].value

    @patch("app.requests.get")
    def test_with_findings(self, mock_get):
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = {"number": 1, "title": "Test PR", "user": {"login": "dev"}}
        mock_resp1.raise_for_status = MagicMock()
        
        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = [{"filename": "main.py", "patch": "+password = 'abc'", "additions": 1}]
        mock_resp2.raise_for_status = MagicMock()
        
        mock_get.side_effect = [mock_resp1, mock_resp2]
        
        at = AppTest.from_file("app.py").run()
        at.text_input(key="github_token").set_value("ghp_test")
        at.text_input(key="pr_url").set_value("https://github.com/abc/def/pull/1")
        at.button(key="run_btn").click().run()
        
        # Check that markdown renders the badge
        # In AppTest, markdown elements are accessible
        assert any("Possible hardcoded password" in md.value for md in at.markdown)
