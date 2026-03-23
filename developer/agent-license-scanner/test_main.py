from main import run, check_compatibility, format_report


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
    issues = [{"package": "x", "version": "1.0", "issue": "COPYLEFT_IN_PERMISSIVE", "message": "bad"}]
    report = format_report(deps, issues)
    assert "issue" in report.lower()
