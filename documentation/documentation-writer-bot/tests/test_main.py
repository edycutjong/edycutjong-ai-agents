import os
import sys
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

runner = CliRunner()

@pytest.fixture
def mock_dependencies():
    with patch('main.FileScanner') as mock_scanner, \
         patch('main.DocGenerator') as mock_generator, \
         patch('main.GitHandler') as mock_git:

        scanner_instance = mock_scanner.return_value
        generator_instance = mock_generator.return_value
        git_instance = mock_git.return_value

        yield scanner_instance, generator_instance, git_instance

def test_run_command_no_files(mock_dependencies):
    scanner, generator, git = mock_dependencies
    scanner.get_source_files.return_value = []
    git.is_git_repo.return_value = True

    result = runner.invoke(app, ["--target-dir", "."])

    assert result.exit_code == 0
    assert "No source files found" in result.stdout

def test_run_command_success(mock_dependencies):
    scanner, generator, git = mock_dependencies
    scanner.get_source_files.return_value = ["file1.py"]
    git.is_git_repo.return_value = True

    generator.generate_doc.return_value = "Doc content"
    generator.generate_mermaid.return_value = "Mermaid content"
    generator.generate_api_ref.return_value = "API content"

    with patch("builtins.open", new_callable=MagicMock()) as mock_open:
        # We need to mock open to avoid writing to disk, or use fs fixture.
        # But main.py uses open() directly.
        # Also need to mock os.makedirs.

        with patch("os.makedirs") as mock_makedirs:
             result = runner.invoke(app, ["--target-dir", ".", "--dry-run"])

    assert result.exit_code == 0
    assert "Documentation generation complete" in result.stdout
    generator.generate_doc.assert_called_with("file1.py")

def test_run_with_commit(mock_dependencies):
    scanner, generator, git = mock_dependencies
    scanner.get_source_files.return_value = ["file1.py"]
    git.is_git_repo.return_value = True
    git.has_changes.return_value = True
    git.commit_changes.return_value = True

    generator.generate_doc.return_value = "Doc"
    generator.generate_mermaid.return_value = ""
    generator.generate_api_ref.return_value = ""

    with patch("builtins.open", new_callable=MagicMock()), \
         patch("os.makedirs"):
        result = runner.invoke(app, ["--target-dir", ".", "--commit"])

    assert result.exit_code == 0
    assert "Committing changes..." in result.stdout
    git.commit_changes.assert_called()

def test_commit_not_git_repo(mock_dependencies):
    scanner, generator, git = mock_dependencies
    git.is_git_repo.return_value = False

    result = runner.invoke(app, ["--target-dir", ".", "--commit"])

    assert result.exit_code == 1
    assert "Error: Target directory is not a git repository" in result.stdout

def test_verbose_mode(mock_dependencies):
    scanner, generator, git = mock_dependencies
    scanner.get_source_files.return_value = ["file1.py"]
    git.is_git_repo.return_value = True
    generator.generate_doc.return_value = "Doc"
    generator.generate_mermaid.return_value = ""
    generator.generate_api_ref.return_value = ""

    with patch("builtins.open", new_callable=MagicMock()), \
         patch("os.makedirs"):
        result = runner.invoke(app, ["--target-dir", ".", "--verbose", "--dry-run"])

    assert result.exit_code == 0
    # Rich output is hard to assert exactly, but we can check if it ran without error
    # and maybe check for parts of the preview.
    # Since we mocked open, the preview relies on full_content which is constructed in main.
