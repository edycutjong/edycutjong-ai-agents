from main import run, analyze_npm, analyze_pip, format_report


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


def test_format_empty():
    assert "look good" in format_report([])


def test_format_findings():
    report = format_report([{"package": "x", "type": "SECURITY", "advice": "upgrade", "severity": "HIGH"}])
    assert "SECURITY" in report
