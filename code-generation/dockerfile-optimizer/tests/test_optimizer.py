"""Tests for Dockerfile Optimizer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.optimizer import analyze_dockerfile, format_analysis_markdown

GOOD_DOCKERFILE = """FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app .
USER appuser
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/ || exit 1
CMD ["python", "main.py"]
"""

BAD_DOCKERFILE = """FROM python
MAINTAINER john@example.com
ADD . /app
RUN apt-get update
RUN apt-get install curl
RUN pip install flask
RUN pip install requests
CMD python app.py
"""

# --- Good Dockerfile ---
def test_good_score():
    r = analyze_dockerfile(GOOD_DOCKERFILE)
    assert r.score >= 70

def test_multi_stage():
    r = analyze_dockerfile(GOOD_DOCKERFILE)
    assert r.stages == 2

def test_has_healthcheck():
    r = analyze_dockerfile(GOOD_DOCKERFILE)
    assert r.has_healthcheck

def test_has_user():
    r = analyze_dockerfile(GOOD_DOCKERFILE)
    assert r.has_user

# --- Bad Dockerfile ---
def test_bad_score():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    assert r.score < 60

def test_detects_untagged():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    ids = [i.rule_id for i in r.issues]
    assert "DL3006" in ids

def test_detects_maintainer():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    ids = [i.rule_id for i in r.issues]
    assert "DL4000" in ids

def test_detects_add():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    ids = [i.rule_id for i in r.issues]
    assert "DL3020" in ids

def test_detects_unpinned_pip():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    ids = [i.rule_id for i in r.issues]
    assert "DL3013" in ids

def test_detects_cmd_format():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    ids = [i.rule_id for i in r.issues]
    assert "DL3025" in ids

def test_no_healthcheck():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    assert not r.has_healthcheck

def test_no_user():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    assert not r.has_user

# --- Output ---
def test_format_markdown():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    md = format_analysis_markdown(r)
    assert "Dockerfile Analysis" in md
    assert "Score" in md

def test_to_dict():
    r = analyze_dockerfile(BAD_DOCKERFILE)
    d = r.to_dict()
    assert "score" in d
    assert "issues" in d

# --- Edge ---
def test_empty():
    r = analyze_dockerfile("")
    assert r.score >= 50

def test_score_bounded():
    for df in [GOOD_DOCKERFILE, BAD_DOCKERFILE, ""]:
        r = analyze_dockerfile(df)
        assert 0 <= r.score <= 100
