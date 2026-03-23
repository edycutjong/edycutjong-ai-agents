from main import run, analyze_dockerfile, format_report


def test_run():
    assert "Docker Slimmer" in run("test")


def test_large_base():
    findings = analyze_dockerfile("FROM python:3.11\nRUN echo hi")
    codes = [f["code"] for f in findings]
    assert "LARGE_BASE" in codes


def test_alpine_ok():
    findings = analyze_dockerfile("FROM python:3.11-alpine\nRUN echo hi")
    codes = [f["code"] for f in findings]
    assert "LARGE_BASE" not in codes


def test_no_recommends():
    findings = analyze_dockerfile("FROM ubuntu\nRUN apt-get install python3")
    codes = [f["code"] for f in findings]
    assert "NO_RECOMMENDS" in codes


def test_copy_all():
    findings = analyze_dockerfile("FROM node:20-slim\nCOPY . .")
    codes = [f["code"] for f in findings]
    assert "COPY_ALL" in codes


def test_pip_cache():
    findings = analyze_dockerfile("FROM python:3.11-slim\nRUN pip install flask")
    codes = [f["code"] for f in findings]
    assert "PIP_CACHE" in codes


def test_clean_dockerfile():
    out = format_report([])
    assert "optimized" in out.lower()


def test_format_findings():
    report = format_report([{"line": 1, "code": "TEST", "message": "test msg", "content": ""}])
    assert "TEST" in report
