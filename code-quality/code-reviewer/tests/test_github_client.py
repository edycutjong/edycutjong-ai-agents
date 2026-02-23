import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.github_client import GitHubClient
from agent_config import Config

@pytest.fixture
def mock_config():
    with patch('agent_config.Config.validate') as mock_validate:
        with patch.object(Config, 'GITHUB_TOKEN', 'fake_token'):
            yield

@patch('src.github_client.Github')
def test_github_client_initialization(mock_github, mock_config):
    client = GitHubClient()
    mock_github.assert_called_once_with('fake_token')

@patch('src.github_client.Github')
@patch('src.github_client.requests')
def test_get_pr_diff(mock_requests, mock_github, mock_config):
    client = GitHubClient()

    mock_repo = MagicMock()
    mock_pr = MagicMock()
    mock_pr.url = 'https://api.github.com/repos/owner/repo/pulls/1'

    mock_github.return_value.get_repo.return_value = mock_repo
    mock_repo.get_pull.return_value = mock_pr

    mock_response = MagicMock()
    mock_response.text = 'diff content'
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response

    diff = client.get_pr_diff('owner/repo', 1)

    assert diff == 'diff content'
    mock_requests.get.assert_called_once()
    assert mock_requests.get.call_args[1]['headers']['Accept'] == 'application/vnd.github.v3.diff'

@patch('src.github_client.Github')
def test_post_comment(mock_github, mock_config):
    client = GitHubClient()

    mock_repo = MagicMock()
    mock_pr = MagicMock()

    mock_github.return_value.get_repo.return_value = mock_repo
    mock_repo.get_pull.return_value = mock_pr

    client.post_comment('owner/repo', 1, 'comment body')

    mock_pr.create_issue_comment.assert_called_once_with('comment body')
