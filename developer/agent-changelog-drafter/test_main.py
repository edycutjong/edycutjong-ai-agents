from main import run, parse_commits, format_changelog


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
