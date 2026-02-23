"""Tests for Dependency Updater."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.updater import parse_requirements, parse_package_json, analyze_dependencies, format_result_markdown

REQ = """flask==2.3.0
requests>=2.28.0
pytest
python-dotenv~=1.0
"""

def test_parse_requirements():
    deps = parse_requirements(REQ)
    assert len(deps) == 4

def test_parse_pinned():
    deps = parse_requirements(REQ)
    flask = [d for d in deps if d.name == "flask"][0]
    assert flask.constraint == "==" and flask.current_version == "2.3.0"

def test_parse_min_version():
    deps = parse_requirements(REQ)
    req = [d for d in deps if d.name == "requests"][0]
    assert req.constraint == ">="

def test_parse_no_version():
    deps = parse_requirements(REQ)
    pt = [d for d in deps if d.name == "pytest"][0]
    assert pt.current_version == ""

def test_parse_comments():
    deps = parse_requirements("# comment\nflask==1.0\n# another\n")
    assert len(deps) == 1

def test_parse_package_json():
    pkg = {"dependencies": {"react": "^18.2.0", "next": "~14.0.0"}, "devDependencies": {"jest": "^29.0.0"}}
    deps = parse_package_json(pkg)
    assert len(deps) == 3

def test_pkg_json_caret():
    pkg = {"dependencies": {"react": "^18.2.0"}}
    deps = parse_package_json(pkg)
    assert deps[0].constraint == "^"

def test_pkg_json_dev():
    pkg = {"dependencies": {}, "devDependencies": {"jest": "^29.0.0"}}
    deps = parse_package_json(pkg)
    assert deps[0].is_dev

def test_analyze_pinned():
    deps = parse_requirements(REQ)
    r = analyze_dependencies(deps)
    assert r.pinned >= 1

def test_analyze_unpinned():
    deps = parse_requirements(REQ)
    r = analyze_dependencies(deps)
    assert r.unpinned >= 1

def test_no_version_issue():
    deps = parse_requirements("flask\nrequests\n")
    r = analyze_dependencies(deps)
    assert any("without version" in i for i in r.issues)

def test_security_suggestion():
    deps = parse_requirements("pyyaml==6.0")
    r = analyze_dependencies(deps)
    assert any("safe_load" in s for s in r.suggestions)

def test_format():
    deps = parse_requirements(REQ)
    r = analyze_dependencies(deps)
    md = format_result_markdown(r)
    assert "Dependency Analysis" in md

def test_to_dict():
    deps = parse_requirements(REQ)
    r = analyze_dependencies(deps)
    d = r.to_dict()
    assert "total_deps" in d

def test_dev_filename():
    deps = parse_requirements("pytest\n", filename="requirements-dev.txt")
    assert deps[0].is_dev
