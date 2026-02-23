import os
import pytest
from agent.reporter import ReportGenerator

@pytest.fixture
def reporter(tmp_path):
    output_dir = tmp_path / "reports"
    return ReportGenerator(output_dir=str(output_dir))

def test_generate_markdown(reporter):
    report_data = {
        "summary": "Test Summary",
        "severity": "HIGH",
        "anomalies": ["Error 1", "Error 2"],
        "root_cause": "Test Root Cause",
        "remediation": "Test Remediation"
    }
    markdown_content = reporter.generate_markdown(report_data)

    assert "# Incident Report" in markdown_content
    assert "Test Summary" in markdown_content
    assert "- Error 1" in markdown_content

def test_save_markdown(reporter):
    filename = "test_report.md"
    content = "# Test Content"
    filepath = reporter.save_markdown(filename, content)

    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        assert f.read() == content

def test_save_pdf(reporter):
    filename = "test_report.pdf"
    content = "# Test Content"
    filepath = reporter.save_pdf(filename, content)

    assert os.path.exists(filepath)
