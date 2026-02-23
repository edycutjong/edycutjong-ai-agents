import pytest
import os
import json
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.reporter import Reporter

def test_generate_report_json(tmp_path):
    reporter = Reporter(output_dir=str(tmp_path))
    results = [{"src": "img.jpg", "suggested_alt": "Alt text"}]
    output_path = reporter.generate_report(results, format="json")

    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        data = json.load(f)
        assert data[0]['src'] == "img.jpg"

def test_generate_report_markdown(tmp_path):
    reporter = Reporter(output_dir=str(tmp_path))
    results = [{"src": "img.jpg", "suggested_alt": "Alt text", "filepath": "test.html"}]
    output_path = reporter.generate_report(results, format="markdown")

    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        content = f.read()
        assert "**Source:** `img.jpg`" in content
