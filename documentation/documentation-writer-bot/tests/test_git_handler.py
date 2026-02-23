import os
import shutil
import tempfile
import pytest
import sys
from git import Repo

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.git_handler import GitHandler

@pytest.fixture
def temp_git_repo():
    temp_dir = tempfile.mkdtemp()

    # Initialize git repo
    repo = Repo.init(temp_dir)

    # Configure git user for commits
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")

    # Initial commit
    file_path = os.path.join(temp_dir, "README.md")
    with open(file_path, "w") as f:
        f.write("# Test Repo")
    repo.index.add([file_path])
    repo.index.commit("Initial commit")

    yield temp_dir
    shutil.rmtree(temp_dir)

def test_is_git_repo(temp_git_repo):
    handler = GitHandler(temp_git_repo)
    assert handler.is_git_repo()

def test_not_git_repo():
    temp_dir = tempfile.mkdtemp()
    handler = GitHandler(temp_dir)
    assert not handler.is_git_repo()
    shutil.rmtree(temp_dir)

def test_has_changes(temp_git_repo):
    handler = GitHandler(temp_git_repo)
    assert not handler.has_changes()

    # Modify a file
    with open(os.path.join(temp_git_repo, "README.md"), "a") as f:
        f.write("\nUpdate")

    assert handler.has_changes()

def test_commit_changes(temp_git_repo):
    handler = GitHandler(temp_git_repo)

    # Create a new file
    with open(os.path.join(temp_git_repo, "new_file.txt"), "w") as f:
        f.write("New content")

    assert handler.has_changes()

    success = handler.commit_changes("Add new file")
    assert success
    assert not handler.has_changes()

    repo = Repo(temp_git_repo)
    commits = list(repo.iter_commits())
    assert commits[0].message == "Add new file"

def test_git_commit_error(temp_git_repo):
    handler = GitHandler(temp_git_repo)

    from git import GitCommandError
    from unittest.mock import MagicMock

    # Replace repo with a Mock
    handler.repo = MagicMock()
    handler.repo.index.commit.side_effect = GitCommandError("cmd", "status")

    success = handler.commit_changes("Fail")
    assert not success

def test_git_general_error(temp_git_repo):
    handler = GitHandler(temp_git_repo)
    from unittest.mock import MagicMock

    # Replace repo with a Mock
    handler.repo = MagicMock()
    handler.repo.index.commit.side_effect = Exception("General error")

    success = handler.commit_changes("Fail")
    assert not success
