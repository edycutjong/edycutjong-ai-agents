from main import run, parse_conflicts, suggest_resolution, format_report


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


def test_format_no_conflicts():
    assert "No merge conflicts" in format_report([])


def test_format_with_conflicts():
    conflicts = parse_conflicts(SAMPLE_CONFLICT)
    report = format_report(conflicts)
    assert "conflict" in report.lower()
