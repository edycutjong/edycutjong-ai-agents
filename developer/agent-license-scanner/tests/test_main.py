import pytest
from unittest.mock import patch
from main import run, check_compatibility, format_report, scan_npm, scan_pip, main


def test_run():
    assert "License Scanner" in run("test")


def test_compatible():
    deps = [{"package": "express", "license": "MIT", "version": "4.18.0"}]
    issues = check_compatibility(deps)
    assert len(issues) == 0


def test_copyleft_detected():
    deps = [{"package": "gpl-lib", "license": "GPL-3.0", "version": "1.0.0"}]
    issues = check_compatibility(deps)
    assert len(issues) == 1
    assert issues[0]["issue"] == "COPYLEFT_IN_PERMISSIVE"


def test_unknown_license():
    deps = [{"package": "mystery", "license": "UNKNOWN", "version": "0.1.0"}]
    issues = check_compatibility(deps)
    assert any(i["issue"] == "UNKNOWN_LICENSE" for i in issues)


def test_format_clean():
    report = format_report([{"package": "x", "license": "MIT", "version": "1.0"}], [])
    assert "compatible" in report.lower()


def test_format_issues():
    deps = [{"package": "x", "license": "GPL-3.0", "version": "1.0"}]
    issues = [{"package": "x", "version": "1.0", "issue": "COPYLEFT_IN_PERMISSIVE", "message": "bad"},
              {"package": "y", "version": "2.0", "issue": "UNKNOWN_LICENSE", "message": "bad2"}]
    report = format_report(deps, issues)
    assert "issue" in report.lower()


def test_scan_npm_no_node_modules(tmp_path):
    assert scan_npm(str(tmp_path)) == []


def test_scan_npm_with_node_modules(tmp_path):
    nm = tmp_path / "node_modules"
    nm.mkdir()
    
    # hidden dir
    (nm / ".bin").mkdir()
    
    # no package json
    (nm / "pkg1").mkdir()
    
    # valid package.json with dict license
    pkg2 = nm / "pkg2"
    pkg2.mkdir()
    (pkg2 / "package.json").write_text('{"name": "pkg2", "version": "1.0", "license": {"type": "MIT"}}')
    
    # valid package.json with string license
    pkg3 = nm / "pkg3"
    pkg3.mkdir()
    (pkg3 / "package.json").write_text('{"name": "pkg3", "version": "2.0", "license": "GPL-3.0"}')

    # invalid json
    pkg4 = nm / "pkg4"
    pkg4.mkdir()
    (pkg4 / "package.json").write_text('invalid json')

    results = scan_npm(str(tmp_path))
    assert len(results) == 3
    licenses = {r["package"]: r["license"] for r in results}
    assert licenses["pkg2"] == "MIT"
    assert licenses["pkg3"] == "GPL-3.0"
    assert licenses["pkg4"] == "PARSE_ERROR"


def test_scan_pip_no_reqs(tmp_path):
    assert scan_pip(str(tmp_path)) == []


def test_scan_pip_with_reqs(tmp_path):
    req = tmp_path / "requirements.txt"
    req.write_text("# header\nflask==1.0.0\nrequests>=2.0.0\nurllib3<1.26\n\n  \n")
    results = scan_pip(str(tmp_path))
    assert len(results) == 3
    pkgs = [r["package"] for r in results]
    assert "flask" in pkgs
    assert "requests" in pkgs
    assert "urllib3" in pkgs


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_main_no_deps(tmp_path, capsys):
    with patch("sys.argv", ["main.py", str(tmp_path)]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert "No dependencies found" in captured.out


def test_main_with_deps(tmp_path, capsys):
    req = tmp_path / "requirements.txt"
    req.write_text("flask==1.0.0\n")
    with patch("sys.argv", ["main.py", str(tmp_path)]):
        main()
    captured = capsys.readouterr()
    assert "License Scan" in captured.out
