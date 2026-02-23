import sys
import os
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
import pytest

# Add the project root to sys.path so we can import agent and tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import app
from tools.diff_engine import APIChange, ChangeType
from tools.ai_analysis import ImpactAnalysis

runner = CliRunner()

@patch("agent.get_repo")
@patch("agent.get_file_content_from_branch")
@patch("agent.detect_breaking_changes")
@patch("agent.AIAnalyzer")
def test_agent_no_changes(mock_ai, mock_detect, mock_get_content, mock_get_repo):
    # Setup mocks
    mock_get_repo.return_value = MagicMock()
    mock_get_content.return_value = '{"openapi": "3.0.0"}' # base spec
    mock_detect.return_value = [] # no changes

    # Create a dummy spec file
    with runner.isolated_filesystem():
        with open("spec.json", "w") as f:
            f.write('{"openapi": "3.0.0"}')

        result = runner.invoke(app, ["spec.json"])

    assert result.exit_code == 0
    assert "No changes detected" in result.stdout

@patch("agent.get_repo")
@patch("agent.get_file_content_from_branch")
@patch("agent.detect_breaking_changes")
@patch("agent.AIAnalyzer")
def test_agent_breaking_changes(mock_ai, mock_detect, mock_get_content, mock_get_repo):
    # Setup mocks
    mock_get_repo.return_value = MagicMock()
    mock_get_content.return_value = '{"openapi": "3.0.0"}'

    mock_change = APIChange(ChangeType.BREAKING, "Removed path", "paths./users")
    mock_detect.return_value = [mock_change]

    mock_analyzer_instance = mock_ai.return_value
    mock_analyzer_instance.analyze.return_value = ImpactAnalysis(
        summary="Removed /users",
        impact_level="High",
        breaking=True,
        version_bump="MAJOR",
        changelog_entry="- Removed /users"
    )

    with runner.isolated_filesystem():
        with open("spec.json", "w") as f:
            f.write('{"openapi": "3.0.0"}')

        result = runner.invoke(app, ["spec.json", "--block-on-breaking"])

    # Should exit with failure (1) because block-on-breaking is default True
    assert result.exit_code == 1
    assert "Breaking changes detected" in result.stdout
    assert "AI Impact Analysis" in result.stdout
