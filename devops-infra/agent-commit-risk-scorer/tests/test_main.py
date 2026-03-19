import pytest
from click.testing import CliRunner
from main import main
import os
import tempfile
import yaml
import json

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Commit Risk Scorer" in result.output

def test_cli_table_format(mocker, test_config_file):
    runner = CliRunner()
    
    mocker.patch("main.get_changed_files", return_value=["src/auth/login.py", "README.md"])
    mocker.patch("main.get_author_email", return_value="test@example.com")
    mocker.patch("subprocess.run", return_value=type('obj', (object,), {'stdout': '2', 'returncode': 0})())

    result = runner.invoke(main, ["--config", test_config_file, "--format", "table"])
    
    assert result.exit_code == 0
    assert "Commit Risk Score" in result.output
    assert "Criticality" in result.output
    assert "Files Analyzed" in result.output

def test_cli_json_format(mocker, test_config_file):
    runner = CliRunner()
    
    mocker.patch("main.get_changed_files", return_value=["src/auth/login.py"])
    mocker.patch("main.get_author_email", return_value="test@example.com")
    mocker.patch("subprocess.run", return_value=type('obj', (object,), {'stdout': '2', 'returncode': 0})())

    result = runner.invoke(main, ["--config", test_config_file, "--format", "json"])
    
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "score" in data
    assert "criticality" in data
    assert "blast_radius" in data

def test_cli_markdown_format(mocker, test_config_file):
    runner = CliRunner()
    
    mocker.patch("main.get_changed_files", return_value=["src/auth/login.py"])
    mocker.patch("main.get_author_email", return_value="test@example.com")
    mocker.patch("subprocess.run", return_value=type('obj', (object,), {'stdout': '2', 'returncode': 0})())

    result = runner.invoke(main, ["--config", test_config_file, "--format", "markdown"])
    
    assert result.exit_code == 0
    assert "## Commit Risk Analysis" in result.output
    assert "| Risk Vector | Score |" in result.output

def test_cli_no_files_changed(mocker, test_config_file):
    runner = CliRunner()
    
    mocker.patch("main.get_changed_files", return_value=[])
    mocker.patch("main.get_author_email", return_value="test@example.com")

    result = runner.invoke(main, ["--config", test_config_file, "--format", "table"])
    
    assert result.exit_code == 0
    assert "No files changed." in result.output

def test_cli_threshold_failure(mocker, test_config_file):
    runner = CliRunner()
    
    # Mock scorer to return a high score
    mocker.patch("main.calculate_total_risk", return_value={
        "score": 80.0,
        "criticality": 30.0,
        "blast_radius": 30.0,
        "coverage_gap": 20.0,
        "history_risk": 0.0,
        "familiarity_discount": 0.0
    })
    
    mocker.patch("main.get_changed_files", return_value=["src/core.py"])
    mocker.patch("main.get_author_email", return_value="test@example.com")

    # threshold defaults to 75 in test_config_file
    result = runner.invoke(main, ["--config", test_config_file, "--format", "json"])
    
    assert result.exit_code == 1 # Exits with 1 due to threshold violation
    
def test_cli_missing_config(mocker):
    runner = CliRunner()
    
    mocker.patch("main.get_changed_files", return_value=["src/core.py"])
    mocker.patch("main.get_author_email", return_value="test@example.com")
    mocker.patch("subprocess.run", return_value=type('obj', (object,), {'stdout': '2', 'returncode': 0})())

    # Ensure config file doesn't exist
    result = runner.invoke(main, ["--config", "nonexistent_config.yaml", "--format", "json"])
    
    assert result.exit_code == 0 # Default threshold is 75, without config scores are likely low
    data = json.loads(result.output)
    assert "score" in data
