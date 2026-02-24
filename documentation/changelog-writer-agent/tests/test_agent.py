import pytest
from unittest.mock import MagicMock, patch



@patch("src.git_utils.git.Repo")
def test_get_commits(mock_repo_class):
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo

    mock_commit = MagicMock()
    mock_commit.hexsha = "abcdef1234567890"
    mock_commit.author.name = "Test Author"
    mock_commit.committed_date = 1678886400
    mock_commit.message = "feat: added login"
    mock_commit.stats.files = {"src/login.py": 10}

    mock_repo.iter_commits.return_value = iter([mock_commit])

    from src.git_utils import get_commits
    commits = get_commits(".")
    assert len(commits) == 1
    assert commits[0]["hash"] == "abcdef1234567890"
    assert commits[0]["message"] == "feat: added login"


def test_format_commits():
    from src.git_utils import format_commits_for_agent
    commits = [{
        "hash": "abcdef1234567890",
        "short_hash": "abcdef1",
        "author": "Test",
        "date": "2023-03-15",
        "message": "feat: login",
        "files_changed": ["src/login.py"],
    }]
    formatted = format_commits_for_agent(commits)
    assert "abcdef1" in formatted
    assert "feat: login" in formatted


@patch("src.agent.genai")
def test_generate_changelog(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = "# Changelog\n\n## 2024-01-01\n\n### New Features\n- Added login"
    mock_model.generate_content.return_value = mock_response

    from src.agent import ChangelogWriterAgent
    agent = ChangelogWriterAgent()
    result = agent.generate("- [abc] feat: login")

    assert "Changelog" in result
    assert "login" in result
    mock_model.generate_content.assert_called_once()
