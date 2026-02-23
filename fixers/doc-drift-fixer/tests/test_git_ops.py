import pytest
from unittest.mock import MagicMock, patch
from tools.git_ops import GitHandler, PRHandler

@pytest.fixture
def mock_repo():
    with patch('tools.git_ops.Repo') as MockRepo:
        repo_instance = MockRepo.return_value
        repo_instance.active_branch.name = 'feature-branch'
        repo_instance.git.diff.return_value = 'diff content'
        yield repo_instance

def test_git_handler_init(mock_repo):
    handler = GitHandler()
    assert handler.repo == mock_repo

def test_get_current_branch(mock_repo):
    handler = GitHandler()
    assert handler.get_current_branch() == 'feature-branch'

def test_get_diff(mock_repo):
    handler = GitHandler()
    diff = handler.get_diff('main')
    assert diff == 'diff content'
    mock_repo.git.diff.assert_called_with('main')

def test_list_changed_files(mock_repo):
    mock_repo.git.diff.return_value = "file1.py\nfile2.py"
    handler = GitHandler()
    files = handler.list_changed_files('main')
    assert files == ['file1.py', 'file2.py']

@patch('tools.git_ops.Github')
def test_pr_handler_post_comment(MockGithub):
    mock_gh = MockGithub.return_value
    mock_repo = mock_gh.get_repo.return_value
    mock_pr = mock_repo.get_pull.return_value

    handler = PRHandler('owner/repo', 1, 'token')
    handler.post_comment('Test Comment')

    mock_gh.get_repo.assert_called_with('owner/repo')
    mock_repo.get_pull.assert_called_with(1)
    mock_pr.create_issue_comment.assert_called_with('Test Comment')

@patch('tools.git_ops.Github')
def test_pr_handler_methods(MockGithub):
     mock_gh = MockGithub.return_value
     mock_repo = mock_gh.get_repo.return_value
     mock_pr = mock_repo.get_pull.return_value

     # Mock files
     mock_file = MagicMock()
     mock_file.filename = "file.py"
     mock_file.patch = "diff"
     mock_pr.get_files.return_value = [mock_file]

     handler = PRHandler('owner/repo', 1, 'token')

     files = handler.get_changed_files()
     assert files == ["file.py"]

     patch_content = handler.get_file_patch("file.py")
     assert patch_content == "diff"

     patch_content_none = handler.get_file_patch("other.py")
     assert patch_content_none == ""
