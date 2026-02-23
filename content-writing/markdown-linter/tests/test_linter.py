"""Tests for Markdown Linter."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.linter import lint_markdown, get_issues_by_rule, format_result_markdown, RULES

CLEAN = "# Title\n\n## Section\n\nSome text here.\n"
TRAILING = "# Title  \n\n## Section\n"
BLANK = "# Title\n\n\n## Section\n"
BAD_HEADING = "#Title\n\nSome text.\n"
SKIP_HEADING = "# H1\n\n### H3\n"
DUP_HEADING = "# Title\n\n## Section\n\n## Section\n"

def test_clean_valid(): r = lint_markdown(CLEAN); assert r.is_valid and r.errors == 0
def test_clean_no_warnings(): r = lint_markdown(CLEAN); assert r.warnings == 0
def test_trailing(): r = lint_markdown(TRAILING); assert r.warnings >= 1
def test_trailing_rule(): r = lint_markdown(TRAILING); assert any(i.rule == "no-trailing-spaces" for i in r.issues)
def test_blank_lines(): r = lint_markdown(BLANK); assert any(i.rule == "no-multiple-blanks" for i in r.issues)
def test_heading_no_space(): r = lint_markdown(BAD_HEADING); assert r.errors >= 1
def test_heading_rule(): r = lint_markdown(BAD_HEADING); assert any(i.rule == "heading-style" for i in r.issues)
def test_heading_skip(): r = lint_markdown(SKIP_HEADING); assert any(i.rule == "heading-increment" for i in r.issues)
def test_dup_heading(): r = lint_markdown(DUP_HEADING); assert any(i.rule == "no-duplicate-heading" for i in r.issues)
def test_line_number(): r = lint_markdown(TRAILING); assert r.issues[0].line == 1
def test_total_lines(): r = lint_markdown(CLEAN); assert r.total_lines >= 5
def test_by_rule(): d = get_issues_by_rule(lint_markdown(TRAILING)); assert "no-trailing-spaces" in d
def test_empty(): r = lint_markdown(""); assert r.total_lines >= 0
def test_warnings_count(): r = lint_markdown(TRAILING + BLANK); assert isinstance(r.warnings, int)
def test_rules(): assert len(RULES) >= 5
def test_format(): md = format_result_markdown(lint_markdown(CLEAN)); assert "Markdown Lint" in md
def test_to_dict(): d = lint_markdown(CLEAN).to_dict(); assert "is_valid" in d
