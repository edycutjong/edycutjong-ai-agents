import pytest
import os
import sys
from typer.testing import CliRunner

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import app

runner = CliRunner()

@pytest.fixture
def fixtures_dir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tests/fixtures')

def test_scan_command(fixtures_dir, tmp_path):
    directory = fixtures_dir
    css_file = os.path.join(fixtures_dir, 'sample.css')
    report_file = tmp_path / "report.html"

    result = runner.invoke(app, ["scan", directory, css_file, "--output-report", str(report_file)])

    assert result.exit_code == 0
    assert "Scan Results" in result.stdout
    assert "Unused Rules" in result.stdout
    assert os.path.exists(report_file)

def test_purge_command(fixtures_dir, tmp_path):
    directory = fixtures_dir
    css_file = os.path.join(fixtures_dir, 'sample.css')
    output_file = tmp_path / "clean.css"

    result = runner.invoke(app, ["purge", css_file, str(output_file), "--directory", directory])

    assert result.exit_code == 0
    assert "Cleaned CSS saved" in result.stdout
    assert os.path.exists(output_file)
    content = output_file.read_text()
    assert ".unused-class" not in content
    assert ".header" in content
