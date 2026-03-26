import pytest
from unittest.mock import patch
from main import run, parse_conflicts, suggest_resolution, format_report, resolve_file, main


SAMPLE_CONFLICT = """line before
<<<<<<< HEAD
our change
=======
their change
>>>>>>> feature-branch
line after"""


def test_run():
    assert "Git Conflict Resolver" in run("test")


def test_parse_conflicts():
    conflicts = parse_conflicts(SAMPLE_CONFLICT)
    assert len(conflicts) == 1
    assert conflicts[0]["ours"] == ["our change"]
    assert conflicts[0]["theirs"] == ["their change"]


def test_no_conflicts():
    assert parse_conflicts("clean file\nno conflicts") == []


def test_suggest_empty_ours():
    c = {"ours": [], "theirs": ["code"]}
    assert suggest_resolution(c) == "ACCEPT_THEIRS"


def test_suggest_empty_theirs():
    c = {"ours": ["code"], "theirs": []}
    assert suggest_resolution(c) == "ACCEPT_OURS"


def test_suggest_identical():
    c = {"ours": ["same"], "theirs": ["same"]}
    assert suggest_resolution(c) == "IDENTICAL"


def test_suggest_prefer_ours():
    c = {"ours": ["1", "2", "3", "4", "5", "6"], "theirs": ["1"]}
    assert suggest_resolution(c) == "PREFER_OURS"


def test_suggest_prefer_theirs():
    c = {"ours": ["1"], "theirs": ["1", "2", "3", "4", "5", "6"]}
    assert suggest_resolution(c) == "PREFER_THEIRS"


def test_resolve_file_no_conflicts():
    assert resolve_file("clean file") == "clean file"


def test_resolve_file_strategy_ours():
    content = "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> feature\n"
    assert resolve_file(content, "ours") == "ours\n"


def test_resolve_file_strategy_theirs():
    content = "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> feature\n"
    assert resolve_file(content, "theirs") == "theirs\n"


def test_resolve_file_strategy_auto_prefer_ours():
    content = "<<<<<<< HEAD\nours\nours\nours\nours\n=======\ntheirs\n>>>>>>> feature\n"
    assert resolve_file(content, "auto") == "ours\nours\nours\nours\n"


def test_resolve_file_strategy_auto_prefer_theirs():
    content = "<<<<<<< HEAD\nours\n=======\ntheirs\ntheirs\ntheirs\ntheirs\n>>>>>>> feature\n"
    assert resolve_file(content, "auto") == "theirs\ntheirs\ntheirs\ntheirs\n"


def test_format_no_conflicts():
    assert "No merge conflicts" in format_report([])


def test_format_with_conflicts():
    conflicts = parse_conflicts(SAMPLE_CONFLICT)
    report = format_report(conflicts)
    assert "conflict" in report.lower()


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_main_success(capsys, tmp_path):
    p = tmp_path / "conflict.txt"
    p.write_text("<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "Found 1 conflict" in captured.out
