import pytest
from unittest.mock import patch
from main import run, analyze_dockerfile, format_report, main


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


def test_npm_dev():
    findings = analyze_dockerfile("FROM node\nRUN npm install express")
    codes = [f["code"] for f in findings]
    assert "NPM_DEV" in codes


def test_layer_merge():
    findings = analyze_dockerfile("FROM node\nRUN curl -O url && tar xzf file")
    codes = [f["code"] for f in findings]
    assert "LAYER_MERGE" in codes


def test_multistage_and_too_many_layers():
    dockerfile = "FROM ubuntu\n" + "RUN echo hi\n" * 6
    findings = analyze_dockerfile(dockerfile)
    codes = [f["code"] for f in findings]
    assert "MULTISTAGE" in codes
    assert "TOO_MANY_LAYERS" in codes


def test_no_cleanup():
    dockerfile = "FROM ubuntu\nRUN apt-get install curl\n"
    findings = analyze_dockerfile(dockerfile)
    codes = [f["code"] for f in findings]
    assert "NO_CLEANUP" in codes


def test_clean_dockerfile():
    out = format_report([])
    assert "optimized" in out.lower()


def test_format_findings():
    report = format_report([{"line": 1, "code": "TEST", "message": "test msg", "content": ""}])
    assert "TEST" in report


def test_format_general():
    report = format_report([{"line": 0, "code": "TEST", "message": "msg", "content": ""}])
    assert "General" in report


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", "non_existent_Dockerfile"])
def test_main_bad_file(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_main_success(capsys, tmp_path):
    p = tmp_path / "Dockerfile"
    p.write_text("FROM python:3.11-alpine\nRUN echo hi")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "optimized" in captured.out
