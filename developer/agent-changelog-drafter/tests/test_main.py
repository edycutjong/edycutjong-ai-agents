from main import run, parse_commits, format_changelog, get_git_log, main
import pytest
from unittest.mock import patch, MagicMock


def test_run():
    assert "Changelog Drafter" in run("test")


def test_parse_conventional():
    log = "abc1234 feat(auth): add login\ndef5678 fix: resolve crash"
    sections = parse_commits(log)
    assert "Features" in sections
    assert "Bug Fixes" in sections


def test_parse_non_conventional():
    sections = parse_commits("update readme")
    assert "Other" in sections


def test_format_changelog():
    sections = {"Features": [{"scope": "api", "message": "add endpoint"}]}
    out = format_changelog("1.0.0", sections)
    assert "1.0.0" in out
    assert "api" in out


def test_empty_sections():
    out = format_changelog("1.0.0", {})
    assert "1.0.0" in out


@patch("subprocess.run")
def test_get_git_log_success(mock_run):
    mock_run.return_value = MagicMock(stdout="commit1\ncommit2\n")
    log = get_git_log()
    assert log == "commit1\ncommit2"
    mock_run.assert_called_with(["git", "log", "--oneline", "--no-merges"], capture_output=True, text=True, check=True)


@patch("subprocess.run")
def test_get_git_log_with_since(mock_run):
    mock_run.return_value = MagicMock(stdout="commit1\n")
    log = get_git_log("v1.0")
    assert log == "commit1"
    mock_run.assert_called_with(["git", "log", "--oneline", "--no-merges", "v1.0..HEAD"], capture_output=True, text=True, check=True)


@patch("subprocess.run")
def test_get_git_log_error(mock_run):
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, [])
    log = get_git_log()
    assert log == ""


@patch("sys.argv", ["main.py"])
@patch("main.get_git_log")
def test_main_no_commits(mock_get_log, capsys):
    mock_get_log.return_value = ""
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "No commits found." in captured.out


@patch("sys.argv", ["main.py", "--since", "v1.0", "--version", "2.0"])
@patch("main.get_git_log")
def test_main_with_commits(mock_get_log, capsys):
    mock_get_log.return_value = "fix(auth): resolve bug"
    main()
    captured = capsys.readouterr()
    assert "resolve bug" in captured.out
    assert "2.0" in captured.out
