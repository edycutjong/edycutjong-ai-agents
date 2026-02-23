import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.git_utils import get_commits, format_commits_for_agent

@patch('src.git_utils.git.Repo')
def test_get_commits(mock_repo_class):
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo

    mock_commit = MagicMock()
    mock_commit.hexsha = "abcdef1234567890"
    mock_commit.author.name = "Test Author"
    mock_commit.committed_date = 1678886400 # 2023-03-15
    mock_commit.message = "feat: added login"
    mock_commit.stats.files = {"src/login.py": 10}

    # iter_commits returns an iterator
    mock_repo.iter_commits.return_value = iter([mock_commit])

    commits = get_commits(".")

    assert len(commits) == 1
    assert commits[0]['hash'] == "abcdef1234567890"
    assert commits[0]['message'] == "feat: added login"
    assert commits[0]['files_changed'] == ["src/login.py"]

def test_format_commits():
    commits = [{
        "hash": "abcdef1234567890",
        "author": "Test Author",
        "date": "2023-03-15T12:00:00",
        "message": "feat: added login",
        "files_changed": ["src/login.py"]
    }]

    formatted = format_commits_for_agent(commits)
    assert "Hash: abcdef1" in formatted
    assert "feat: added login" in formatted
