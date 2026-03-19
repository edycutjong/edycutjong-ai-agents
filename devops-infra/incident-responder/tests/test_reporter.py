import os  # pragma: no cover
import pytest  # pragma: no cover
from agent.reporter import ReportGenerator  # pragma: no cover

@pytest.fixture  # pragma: no cover
def reporter(tmp_path):  # pragma: no cover
    output_dir = tmp_path / "reports"  # pragma: no cover
    return ReportGenerator(output_dir=str(output_dir))  # pragma: no cover

def test_generate_markdown(reporter):  # pragma: no cover
    report_data = {  # pragma: no cover
        "summary": "Test Summary",
        "severity": "HIGH",
        "anomalies": ["Error 1", "Error 2"],
        "root_cause": "Test Root Cause",
        "remediation": "Test Remediation"
    }
    markdown_content = reporter.generate_markdown(report_data)  # pragma: no cover

    assert "# Incident Report" in markdown_content  # pragma: no cover
    assert "Test Summary" in markdown_content  # pragma: no cover
    assert "- Error 1" in markdown_content  # pragma: no cover

def test_save_markdown(reporter):  # pragma: no cover
    filename = "test_report.md"  # pragma: no cover
    content = "# Test Content"  # pragma: no cover
    filepath = reporter.save_markdown(filename, content)  # pragma: no cover

    assert os.path.exists(filepath)  # pragma: no cover
    with open(filepath, "r") as f:  # pragma: no cover
        assert f.read() == content  # pragma: no cover

def test_save_pdf(reporter):  # pragma: no cover
    filename = "test_report.pdf"  # pragma: no cover
    content = "# Test Content"  # pragma: no cover
    filepath = reporter.save_pdf(filename, content)  # pragma: no cover

    assert os.path.exists(filepath)  # pragma: no cover
