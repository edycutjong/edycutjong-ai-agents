"""Tests for SemVer Parser."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.parser import parse_semver, bump, is_compatible, sort_versions, satisfies_range, format_result_markdown

def test_parse(): v = parse_semver("1.2.3"); assert v.major == 1 and v.minor == 2 and v.patch == 3
def test_prefix_v(): v = parse_semver("v1.0.0"); assert v.is_valid and v.major == 1
def test_prerelease(): v = parse_semver("1.0.0-alpha.1"); assert v.prerelease == "alpha.1"
def test_build(): v = parse_semver("1.0.0+build.123"); assert v.build == "build.123"
def test_invalid(): v = parse_semver("not-a-version"); assert not v.is_valid
def test_str(): assert str(parse_semver("1.2.3")) == "1.2.3"
def test_str_pre(): assert str(parse_semver("1.0.0-beta")) == "1.0.0-beta"
def test_bump_patch(): v = bump("1.2.3"); assert v.patch == 4 and v.minor == 2
def test_bump_minor(): v = bump("1.2.3", "minor"); assert v.minor == 3 and v.patch == 0
def test_bump_major(): v = bump("1.2.3", "major"); assert v.major == 2 and v.minor == 0
def test_compare_lt(): assert parse_semver("1.0.0") < parse_semver("2.0.0")
def test_compare_eq(): assert parse_semver("1.0.0") == parse_semver("1.0.0")
def test_compatible(): assert is_compatible("1.2.3", "1.9.0")
def test_incompatible(): assert not is_compatible("1.0.0", "2.0.0")
def test_sort(): assert sort_versions(["2.0.0", "1.0.0", "1.5.0"]) == ["1.0.0", "1.5.0", "2.0.0"]
def test_range_caret(): assert satisfies_range("1.5.0", "^1.0.0")
def test_range_tilde(): assert satisfies_range("1.0.5", "~1.0.0")
def test_format(): md = format_result_markdown(parse_semver("1.0.0")); assert "SemVer" in md
def test_to_dict(): d = parse_semver("1.0.0").to_dict(); assert "major" in d
