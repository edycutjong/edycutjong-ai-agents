import pytest
from unittest.mock import patch
from main import run, analyze_query, estimate_complexity, format_report, main


def test_run():
    assert "SQL Query Optimizer" in run("test")


def test_select_star():
    findings, _ = analyze_query("SELECT * FROM users")
    assert any(f["code"] == "SELECT_STAR" for f in findings)


def test_leading_wildcard():
    findings, _ = analyze_query("SELECT name FROM users WHERE name LIKE '%john%'")
    assert any(f["code"] == "LEADING_WILDCARD" for f in findings)


def test_subquery_in():
    findings, _ = analyze_query("SELECT * FROM orders WHERE user_id IN (SELECT id FROM users)")
    codes = [f["code"] for f in findings]
    assert "SUBQUERY_IN" in codes


def test_not_in():
    findings, _ = analyze_query("SELECT id FROM users WHERE id NOT IN (1,2,3)")
    assert any(f["code"] == "NOT_IN" for f in findings)


def test_clean_query():
    findings, _ = analyze_query("SELECT id, name FROM users WHERE id = 1")
    assert len(findings) == 0


def test_index_candidates():
    _, candidates = analyze_query("SELECT id FROM users WHERE email = 'x' ORDER BY created_at")
    assert "email" in candidates
    assert "created_at" in candidates


def test_complexity():
    assert estimate_complexity("SELECT a FROM b") == "LOW"
    assert estimate_complexity("SELECT a FROM b JOIN c ON b.id = c.id JOIN d ON c.id = d.id") == "MEDIUM"


def test_complexity_high():
    assert estimate_complexity("SELECT a FROM b JOIN c ON b.id = c.id JOIN d ON c.id = d.id JOIN e ON d.id = e.id JOIN f ON e.id = f.id") == "HIGH"


def test_format_report():
    findings = [{"code": "SELECT_STAR", "message": "avoid", "severity": "MEDIUM"}]
    report = format_report("SELECT * FROM x", findings, ["col1"])
    assert "SELECT_STAR" in report
    assert "col1" in report


def test_format_no_findings():
    report = format_report("SELECT id FROM users", [], [])
    assert "No common anti-patterns" in report


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_main_with_file(capsys, tmp_path):
    p = tmp_path / "query.sql"
    p.write_text("SELECT * FROM users")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "SELECT_STAR" in captured.out


def test_main_with_string(capsys):
    with patch("sys.argv", ["main.py", "SELECT * FROM users"]):
        main()
    captured = capsys.readouterr()
    assert "SELECT_STAR" in captured.out
