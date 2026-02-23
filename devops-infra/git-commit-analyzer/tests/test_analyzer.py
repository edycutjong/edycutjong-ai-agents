"""Tests for Git Commit Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import parse_commit, parse_commits, analyze_commits, format_analysis_markdown, CONVENTIONAL_TYPES

COMMITS = """abc1234 feat(auth): add login endpoint
def5678 fix: resolve null pointer exception
ghi9012 docs: update API documentation
jkl3456 refactor(db): optimize query performance
mno7890 test: add unit tests for user module
pqr1234 chore: update dependencies
stu5678 feat!: redesign dashboard layout"""

def test_parse_conventional():
    c = parse_commit("abc1234 feat(auth): add login endpoint")
    assert c.is_conventional and c.commit_type == "feat" and c.scope == "auth"

def test_parse_no_scope():
    c = parse_commit("abc1234 fix: resolve bug")
    assert c.is_conventional and c.commit_type == "fix" and c.scope == ""

def test_parse_breaking():
    c = parse_commit("abc1234 feat!: breaking change")
    assert c.is_breaking

def test_parse_non_conventional():
    c = parse_commit("abc1234 updated some stuff")
    assert not c.is_conventional

def test_parse_hash():
    c = parse_commit("abcdef12 fix: bug")
    assert c.hash == "abcdef12"

def test_parse_commits():
    commits = parse_commits(COMMITS)
    assert len(commits) == 7

def test_analyze_total():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.total == 7

def test_conventional_pct():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.conventional_pct == 100.0

def test_type_distribution():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.type_distribution["feat"] == 2

def test_breaking_count():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.breaking_changes == 1

def test_avg_length():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.avg_message_length > 10

def test_score_good():
    a = analyze_commits(parse_commits(COMMITS))
    assert a.score >= 70

def test_score_bad():
    a = analyze_commits(parse_commits("abc fix\ndef up"))
    assert a.score < 50

def test_issues_short():
    a = analyze_commits(parse_commits("abc fix\ndef up"))
    assert any("short" in i for i in a.issues)

def test_format():
    a = analyze_commits(parse_commits(COMMITS))
    md = format_analysis_markdown(a)
    assert "Commit Analysis" in md

def test_conventional_types():
    assert len(CONVENTIONAL_TYPES) >= 10

def test_breaking_keyword():
    c = parse_commit("abc1234 feat: something BREAKING CHANGE here")
    assert c.is_breaking
