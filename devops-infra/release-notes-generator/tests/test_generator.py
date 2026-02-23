"""Tests for Release Notes Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import parse_commit, parse_commits, group_by_type, generate_release_notes, get_stats

COMMITS_TEXT = """abc1234 feat(auth): add OAuth2 support
def5678 fix(api): handle null response
aaa9012 feat: add dark mode
bbb3456 fix(ui): button alignment
ccc7890 docs: update API documentation
ddd1234 perf: optimize database queries
eee5678 feat(auth)!: change token format
fff9012 chore: update dependencies"""

def test_parse_feat():
    c = parse_commit("feat(auth): add login")
    assert c.type == "feat" and c.scope == "auth"

def test_parse_fix():
    c = parse_commit("fix: typo in readme")
    assert c.type == "fix" and c.scope == ""

def test_parse_breaking():
    c = parse_commit("feat(api)!: change response format")
    assert c.breaking

def test_parse_non_conventional():
    c = parse_commit("random commit message")
    assert c.type == "other"

def test_parse_commits():
    commits = parse_commits(COMMITS_TEXT)
    assert len(commits) == 8

def test_parse_with_hash():
    commits = parse_commits(COMMITS_TEXT)
    assert commits[0].hash == "abc1234"

def test_group_by_type():
    commits = parse_commits(COMMITS_TEXT)
    groups = group_by_type(commits)
    assert len(groups["feat"]) == 3

def test_release_notes_has_features():
    commits = parse_commits(COMMITS_TEXT)
    notes = generate_release_notes(commits, version="v1.0.0")
    assert "Features" in notes
    assert "v1.0.0" in notes

def test_release_notes_has_fixes():
    commits = parse_commits(COMMITS_TEXT)
    notes = generate_release_notes(commits)
    assert "Bug Fixes" in notes

def test_breaking_changes_section():
    commits = parse_commits(COMMITS_TEXT)
    notes = generate_release_notes(commits)
    assert "BREAKING CHANGES" in notes

def test_scope_shown():
    commits = parse_commits(COMMITS_TEXT)
    notes = generate_release_notes(commits)
    assert "**auth:**" in notes

def test_hash_shown():
    commits = parse_commits(COMMITS_TEXT)
    notes = generate_release_notes(commits)
    assert "(abc1234)" in notes

def test_stats():
    commits = parse_commits(COMMITS_TEXT)
    s = get_stats(commits)
    assert s["total"] == 8
    assert s["features"] == 3
    assert s["fixes"] == 2
    assert s["breaking"] == 1

def test_commit_to_dict():
    c = parse_commit("feat: hello")
    d = c.to_dict()
    assert d["type"] == "feat"

def test_empty():
    notes = generate_release_notes([], version="v0.0.1")
    assert "v0.0.1" in notes
