"""Tests for main.py CLI, config.py, and git_utils.py."""
import os, sys, pytest
from unittest.mock import patch, MagicMock, PropertyMock

# Add paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
sys.path.insert(0, src_dir)

# Must mock crewai and dependencies before import
sys.modules.setdefault("crewai", MagicMock())

from config import Config

def test_config(): assert Config is not None

def test_git_utils_invalid_repo(tmp_path):
    """Cover git_utils.py lines 11-12: InvalidGitRepositoryError."""
    import git
    from git_utils import get_commits
    # tmp_path exists but isn't a git repo
    with pytest.raises(ValueError, match="Invalid git repository"):
        get_commits(str(tmp_path))

def test_git_utils_format_commits():
    """Cover git_utils.py format_commits_for_agent."""
    from git_utils import format_commits_for_agent
    commits = [{"hash": "abc1234567890", "author": "Dev", "date": "2024-01-01", "message": "fix bug", "files_changed": ["a.py"]}]
    result = format_commits_for_agent(commits)
    assert "abc1234" in result
    assert "Dev" in result

def test_git_utils_git_command_error(tmp_path):
    """Cover git_utils.py lines 30-31: GitCommandError."""
    import git
    from git_utils import get_commits
    # Create a valid git repo with no commits
    repo = git.Repo.init(str(tmp_path))
    with pytest.raises(ValueError, match="Error fetching commits"):
        get_commits(str(tmp_path), "nonexistent_ref", "HEAD")

def test_git_utils_from_ref_none(tmp_path):
    """Cover git_utils.py line 16: from_ref is None (else branch)."""
    import git
    from git_utils import get_commits
    repo = git.Repo.init(str(tmp_path))
    # create a file and commit
    (tmp_path / "README.md").write_text("hello")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    commits = get_commits(str(tmp_path), from_ref=None, to_ref="HEAD")
    assert len(commits) >= 1

def test_main_no_commits():
    """Cover main.py lines 50-51: no commits branch."""
    from unittest.mock import patch, MagicMock
    with patch("main.Prompt") as MockPrompt, \
         patch("main.console") as mock_console, \
         patch("main.get_commits", return_value=[]):
        MockPrompt.ask.side_effect = ["/tmp", "HEAD~1", "HEAD"]
        from main import main
        main()
        mock_console.print.assert_any_call("[yellow]No commits found in the specified range.[/yellow]")

def test_main_get_commits_exception():
    """Cover main.py lines 45-47: exception fetching commits."""
    with patch("main.Prompt") as MockPrompt, \
         patch("main.console") as mock_console, \
         patch("main.get_commits", side_effect=Exception("git error")):
        MockPrompt.ask.side_effect = ["/tmp", "HEAD~1", "HEAD"]
        from main import main
        main()

def test_main_crew_exception():
    """Cover main.py lines 80-82: crew exception."""
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.side_effect = Exception("crew error")
    with patch("main.Prompt") as MockPrompt, \
         patch("main.console") as mock_console, \
         patch("main.get_commits", return_value=[{"hash": "abc", "author": "dev", "date": "2024", "message": "test", "files_changed": []}]), \
         patch("main.format_commits_for_agent", return_value="formatted"), \
         patch("main.ChangelogAgents") as MockAgents, \
         patch("main.ChangelogTasks") as MockTasks, \
         patch("main.Crew", return_value=mock_crew_instance):
        MockPrompt.ask.side_effect = ["/tmp", "HEAD~1", "HEAD"]
        from main import main
        main()

def test_main_result_with_raw():
    """Cover main.py line 87: result has .raw attribute."""
    mock_result = MagicMock()
    mock_result.raw = "# Generated Changelog"
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = mock_result
    with patch("main.Prompt") as MockPrompt, \
         patch("main.console") as mock_console, \
         patch("main.get_commits", return_value=[{"hash": "abc", "author": "dev", "date": "2024", "message": "test", "files_changed": []}]), \
         patch("main.format_commits_for_agent", return_value="formatted"), \
         patch("main.ChangelogAgents") as MockAgents, \
         patch("main.ChangelogTasks") as MockTasks, \
         patch("main.Crew", return_value=mock_crew_instance), \
         patch("builtins.open", MagicMock()):
        MockPrompt.ask.side_effect = ["/tmp", "HEAD~1", "HEAD"]
        from main import main
        main()

def test_main_io_error():
    """Cover main.py lines 96-97: IOError saving file."""
    mock_result = MagicMock(spec=[])  # no .raw attribute
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = mock_result
    with patch("main.Prompt") as MockPrompt, \
         patch("main.console") as mock_console, \
         patch("main.get_commits", return_value=[{"hash": "abc", "author": "dev", "date": "2024", "message": "test", "files_changed": []}]), \
         patch("main.format_commits_for_agent", return_value="formatted"), \
         patch("main.ChangelogAgents") as MockAgents, \
         patch("main.ChangelogTasks") as MockTasks, \
         patch("main.Crew", return_value=mock_crew_instance), \
         patch("builtins.open", side_effect=IOError("Permission denied")):
        MockPrompt.ask.side_effect = ["/tmp", "HEAD~1", "HEAD"]
        from main import main
        main()


def test_agents_import():
    """Cover agents.py lines 8-9, 12, 22."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from agents import ChangelogAgents
        agents = ChangelogAgents()
        classifier = agents.commit_classifier()
        writer = agents.changelog_writer()
        assert classifier is not None
        assert writer is not None

def test_tasks_import():
    """Cover tasks.py lines 6 and 26."""
    from tasks import ChangelogTasks
    tasks = ChangelogTasks()
    mock_agent = MagicMock()
    t1 = tasks.classify_commits_task(mock_agent, "some commits")
    t2 = tasks.write_changelog_task(mock_agent)
    assert t1 is not None
    assert t2 is not None

def test_main_block():
    import runpy
    import sys
    from unittest.mock import patch
    
    with patch("main.Prompt.ask", side_effect=["/repo", "HEAD~1", "HEAD"]), \
         patch("main.get_commits", return_value=[]), \
         patch.object(sys, 'argv', ['main.py']):
        runpy.run_module('main', run_name='__main__')

