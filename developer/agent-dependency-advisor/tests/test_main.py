import pytest
from unittest.mock import patch
from main import run, analyze_npm, analyze_pip, format_report, main


def test_run():
    assert "Dependency Advisor" in run("test")


def test_deprecated_npm():
    data = {"dependencies": {"moment": "^2.29.0"}}
    findings = analyze_npm(data)
    assert any(f["type"] == "DEPRECATED" for f in findings)


def test_security_npm():
    data = {"dependencies": {"lodash": "^4.0.0"}}
    findings = analyze_npm(data)
    assert any(f["type"] == "SECURITY" for f in findings)


def test_unpinned_npm():
    data = {"dependencies": {"express": "*"}}
    findings = analyze_npm(data)
    assert any(f["type"] == "PINNING" for f in findings)


def test_unpinned_pip():
    findings = analyze_pip("flask\nrequests")
    assert len(findings) == 2
    assert all(f["type"] == "PINNING" for f in findings)


def test_pinned_pip():
    findings = analyze_pip("flask==2.3.0\nrequests>=2.28.0")
    assert len(findings) == 0


def test_analyze_pip_comments():
    findings = analyze_pip("   \n# a comment\nrequests==2.0\n")
    assert len(findings) == 0


def test_format_empty():
    assert "look good" in format_report([])


def test_format_findings():
    report = format_report([{"package": "x", "type": "SECURITY", "advice": "upgrade", "severity": "HIGH"}])
    assert "SECURITY" in report


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", "invalid_file_that_does_not_exist.json"])
def test_main_invalid_file(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_main_npm(capsys, tmp_path):
    p = tmp_path / "package.json"
    p.write_text('{"dependencies": {"lodash": "latest"}}')
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "lodash" in captured.out


def test_main_pip(capsys, tmp_path):
    p = tmp_path / "requirements.txt"
    p.write_text('flask\n')
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "flask" in captured.out
