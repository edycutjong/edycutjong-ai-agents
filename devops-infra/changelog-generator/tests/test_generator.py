"""Tests for Changelog Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import parse_commit, generate_changelog, suggest_version_bump, format_changelog_markdown, CATEGORIES

COMMITS = ["feat(auth): add login page", "fix(api): resolve timeout issue", "docs: update README", "feat!: redesign dashboard", "chore: update deps"]

def test_parse_feat(): e = parse_commit("feat(auth): add login"); assert e.type == "feat" and e.scope == "auth"
def test_parse_fix(): e = parse_commit("fix: bug"); assert e.type == "fix" and e.message == "bug"
def test_parse_breaking(): e = parse_commit("feat!: break"); assert e.breaking
def test_parse_no_scope(): e = parse_commit("docs: readme"); assert e.scope == "" and e.type == "docs"
def test_parse_non_conv(): e = parse_commit("random message"); assert e.type == "other"
def test_generate(): r = generate_changelog(COMMITS); assert len(r.entries) == 5
def test_grouped(): r = generate_changelog(COMMITS); assert "Features" in r.grouped
def test_breaking_list(): r = generate_changelog(COMMITS); assert len(r.breaking_changes) >= 1
def test_stats(): r = generate_changelog(COMMITS); assert r.stats.get("feat", 0) >= 1
def test_version(): r = generate_changelog(COMMITS, version="1.0.0"); assert r.version == "1.0.0"
def test_bump_major(): r = generate_changelog(["feat!: break"]); assert suggest_version_bump(r) == "major"
def test_bump_minor(): r = generate_changelog(["feat: new"]); assert suggest_version_bump(r) == "minor"
def test_bump_patch(): r = generate_changelog(["fix: bug"]); assert suggest_version_bump(r) == "patch"
def test_format(): md = format_changelog_markdown(generate_changelog(COMMITS)); assert "Changelog" in md
def test_format_features(): md = format_changelog_markdown(generate_changelog(COMMITS)); assert "Features" in md
def test_format_breaking(): md = format_changelog_markdown(generate_changelog(COMMITS)); assert "Breaking" in md
def test_categories(): assert len(CATEGORIES) >= 8
def test_to_dict(): d = generate_changelog(COMMITS).to_dict(); assert "total" in d
