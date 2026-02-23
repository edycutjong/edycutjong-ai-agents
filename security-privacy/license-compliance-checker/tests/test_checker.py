"""Tests for License Compliance Checker."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.checker import classify_license, normalize_license, check_compatibility, parse_requirements_txt, parse_package_json, format_report_markdown, LicenseInfo, LICENSE_DB

def test_classify_mit(): assert classify_license("MIT") == "permissive"
def test_classify_gpl(): assert classify_license("GPL-3.0") == "copyleft"
def test_classify_agpl(): assert classify_license("AGPL-3.0") == "restrictive"
def test_classify_unknown(): assert classify_license("CustomLicense") == "unknown"
def test_normalize(): assert normalize_license("MIT License") == "MIT"
def test_normalize_apache(): assert normalize_license("Apache License 2.0") == "Apache-2.0"

def test_compatible_permissive():
    deps = [LicenseInfo(name="lib", license="MIT")]
    issues = check_compatibility("MIT", deps)
    assert len(issues) == 0

def test_incompatible_copyleft():
    deps = [LicenseInfo(name="lib", license="GPL-3.0")]
    issues = check_compatibility("MIT", deps)
    assert len(issues) >= 1

def test_parse_requirements():
    deps = parse_requirements_txt("flask\nrequests>=2.0\npytest")
    assert len(deps) == 3
    assert deps[0].name == "flask"

def test_parse_requirements_comments():
    deps = parse_requirements_txt("# comment\nflask\n")
    assert len(deps) == 1

def test_parse_package_json():
    pkg = '{"dependencies": {"express": "^4.0", "cors": "^2.0"}, "devDependencies": {"jest": "^29"}}'
    deps = parse_package_json(pkg)
    assert len(deps) == 3

def test_format_clean():
    deps = [LicenseInfo(name="lib", license="MIT", category="permissive")]
    md = format_report_markdown("MIT", deps, [])
    assert "✅" in md

def test_format_issues():
    deps = [LicenseInfo(name="lib", license="GPL-3.0")]
    issues = check_compatibility("MIT", deps)
    md = format_report_markdown("MIT", deps, issues)
    assert "Issues" in md

def test_license_db_count():
    assert len(LICENSE_DB) >= 15

def test_to_dict():
    li = LicenseInfo(name="test", license="MIT", category="permissive")
    d = li.to_dict()
    assert d["name"] == "test"

def test_multiple_deps():
    deps = [LicenseInfo(name="a", license="MIT"), LicenseInfo(name="b", license="Apache-2.0"), LicenseInfo(name="c", license="GPL-3.0")]
    issues = check_compatibility("MIT", deps)
    assert len(issues) == 1  # only GPL is incompatible
