import os, tempfile
import pytest
from unittest.mock import patch
from main import run, scan_project, detect_framework, generate_guide, main


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


def test_scan_project_unreadable_file(tmp_path):
    p = tmp_path / "app.py"
    p.write_bytes(b'\xff\xfe\x00\x00')
    with patch("builtins.open", side_effect=OSError):
        stats = scan_project(str(tmp_path))
    assert stats["total_lines"] == 0


def test_detect_framework_empty():
    with tempfile.TemporaryDirectory() as td:
        assert detect_framework({}, td) == []


def test_detect_framework_pkg_json(tmp_path):
    p = tmp_path / "package.json"
    p.write_text('{"dependencies": {"react": "^17"}}')
    fws = detect_framework({}, str(tmp_path))
    assert "React" in fws


def test_detect_framework_req_txt(tmp_path):
    p = tmp_path / "requirements.txt"
    p.write_text('django==3.2')
    fws = detect_framework({}, str(tmp_path))
    assert "Django" in fws


def test_detect_framework_oserror(tmp_path):
    p = tmp_path / "package.json"
    p.write_text('')
    r = tmp_path / "requirements.txt"
    r.write_text('')
    with patch("builtins.open", side_effect=OSError):
        fws = detect_framework({}, str(tmp_path))
        assert fws == []


def test_generate_guide():
    stats = {"files": 10, "dirs": 3, "languages": {"Python": 5}, "key_files": ["README.md"], "total_lines": 100}
    guide = generate_guide(stats, ["Flask"])
    assert "Onboarding" in guide
    assert "Flask" in guide
    assert "Python" in guide


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


@patch("sys.argv", ["main.py", "non_existent_dir_12345"])
def test_main_bad_dir(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "not a directory" in captured.out


@patch("sys.argv", ["main.py", "."])
def test_main_success(capsys):
    main()
    captured = capsys.readouterr()
    assert "Onboarding Guide" in captured.out
