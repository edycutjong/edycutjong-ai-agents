from main import run, audit_env, format_report


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


def test_format_empty():
    assert "clean" in format_report([]).lower()


def test_format_findings():
    report = format_report([{"line": 1, "code": "T", "message": "m", "severity": "HIGH"}])
    assert "Env Audit" in report
