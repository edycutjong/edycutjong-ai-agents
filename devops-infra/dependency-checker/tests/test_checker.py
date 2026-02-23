"""Tests for Dependency Checker."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.checker import parse_requirements, find_conflicts, get_package_names, check_security, generate_requirements, format_result_markdown

REQ = "flask==2.0.1\nrequests>=2.25\npytest\nnumpy==1.21\n"
DUP = "flask==2.0\nflask==2.1\n"

def test_total(): r = parse_requirements(REQ); assert r.total == 4
def test_pinned(): r = parse_requirements(REQ); assert r.pinned == 2
def test_unpinned(): r = parse_requirements(REQ); assert r.unpinned == 2
def test_name(): r = parse_requirements(REQ); assert r.packages[0].name == "flask"
def test_version(): r = parse_requirements(REQ); assert r.packages[0].version == "2.0.1"
def test_operator(): r = parse_requirements(REQ); assert r.packages[1].operator == ">="
def test_no_version(): r = parse_requirements(REQ); assert r.packages[2].version == ""
def test_comments(): r = parse_requirements("# comment\nflask\n"); assert r.total == 1
def test_empty(): r = parse_requirements(""); assert r.total == 0
def test_duplicates(): r = parse_requirements(DUP); assert len(r.duplicates) >= 1
def test_conflicts(): c = find_conflicts(DUP); assert "flask" in c
def test_names(): names = get_package_names(REQ); assert "flask" in names
def test_security(): flagged = check_security(["django", "flask"]); assert len(flagged) >= 0
def test_generate(): req = generate_requirements({"flask": "2.0", "pytest": "7.0"}); assert "flask==2.0" in req
def test_format(): md = format_result_markdown(parse_requirements(REQ)); assert "Dependency Checker" in md
def test_to_dict(): d = parse_requirements(REQ).to_dict(); assert "total" in d
