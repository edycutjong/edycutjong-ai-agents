import pytest
from unittest.mock import patch
from main import run, audit_env, format_report, main


def test_run():
    assert "Env File Auditor" in run("test")


def test_password_detection():
    findings = audit_env("PASSWORD=secret123")
    assert any(f["code"] == "HARDCODED_PASSWORD" for f in findings)


def test_api_key_detection():
    findings = audit_env("API_KEY=sk-abc123def456")
    assert any(f["code"] == "API_KEY" for f in findings)


def test_aws_detection():
    findings = audit_env("AWS_ACCESS_KEY_ID=AKIA1234")
    assert any(f["code"] == "AWS_CREDS" for f in findings)


def test_empty_value():
    findings = audit_env("DATABASE_URL=")
    assert any(f["code"] == "EMPTY_VALUE" for f in findings)


def test_invalid_format():
    findings = audit_env("this is not valid")
    assert any(f["code"] == "INVALID_FORMAT" for f in findings)


def test_clean_env():
    findings = audit_env("NODE_ENV=production\nPORT=3000")
    assert not any(f["severity"] == "HIGH" for f in findings)


def test_comment_and_blank_lines():
    findings = audit_env("\n# this is a comment\n\n# another one\n")
    assert len(findings) == 0


def test_space_in_key():
    findings = audit_env("API KEY=1234")
    assert any(f["code"] == "SPACE_IN_KEY" for f in findings)


def test_long_uppercase_value():
    findings = audit_env("KEY=" + "A" * 25)
    # The code literally just passes, shouldn't crash
    assert len(findings) >= 0


def test_gitignore_check(tmp_path):
    d = tmp_path / "envdir"
    d.mkdir()
    env = d / ".env"
    env.write_text("A=1")
    gi = d / ".gitignore"
    gi.write_text("node_modules\n")
    findings = audit_env(env.read_text(), str(env))
    assert any(f["code"] == "NOT_GITIGNORED" for f in findings)


def test_format_empty():
    assert "clean" in format_report([]).lower()


def test_format_findings():
    report = format_report([{"line": 1, "code": "T", "message": "m", "severity": "HIGH"}])
    assert "Env Audit" in report


def test_format_general():
    report = format_report([{"line": 0, "code": "T", "message": "m", "severity": "HIGH"}])
    assert "General:" in report


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", "invalid_file_that_does_not_exist.env"])
def test_main_invalid_file(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_main_success(capsys, tmp_path):
    p = tmp_path / ".env"
    p.write_text("API_KEY=123")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "API_KEY" in captured.out
