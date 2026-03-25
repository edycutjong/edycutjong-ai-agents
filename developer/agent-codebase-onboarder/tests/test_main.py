import os, tempfile
from main import run, scan_project, detect_framework, generate_guide


def test_run():
    assert "Codebase Onboarder" in run("test")


def test_scan_project():
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "app.py"), "w").write("print('hi')\n")
        open(os.path.join(td, "README.md"), "w").write("# Hello\n")
        stats = scan_project(td)
        assert stats["files"] >= 2
        assert "Python" in stats["languages"]
        assert "README.md" in stats["key_files"]


def test_detect_framework_empty():
    with tempfile.TemporaryDirectory() as td:
        assert detect_framework({}, td) == []


def test_generate_guide():
    stats = {"files": 10, "dirs": 3, "languages": {"Python": 5}, "key_files": ["README.md"], "total_lines": 100}
    guide = generate_guide(stats, ["Flask"])
    assert "Onboarding" in guide
    assert "Flask" in guide
    assert "Python" in guide
