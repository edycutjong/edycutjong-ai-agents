"""Tests for the Dead Code Finder Agent."""
import os
import sys
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import analyze_file, scan_directory, format_report, run, main


class TestAnalyzeFile:
    def test_run(self):
        assert "Dead Code Finder" in run("test")

    def test_detect_unused_import(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("import os\nimport sys\nprint('hello')\n")
        result = analyze_file(str(f))
        unused = [i["alias"] for i in result["unused_imports"]]
        assert "os" in unused
        assert "sys" in unused

    def test_detect_used_import(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("import os\nprint(os.getcwd())\n")
        result = analyze_file(str(f))
        unused = [i["alias"] for i in result["unused_imports"]]
        assert "os" not in unused

    def test_import_from(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("from os import path\nfrom sys import argv as a\nprint(path)\n")
        result = analyze_file(str(f))
        unused = [i["alias"] for i in result["unused_imports"]]
        assert "a" in unused

    def test_detect_unused_function(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("def unused_func():\n    pass\n\ndef main():\n    pass\n\nmain()\n")
        result = analyze_file(str(f))
        unused_names = [d["name"] for d in result["unused_defs"]]
        assert "unused_func" in unused_names

    def test_async_function(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("async def foo():\n    pass\nasync def bar():\n    pass\nfoo()\n")
        result = analyze_file(str(f))
        unused_names = [d["name"] for d in result["unused_defs"]]
        assert "bar" in unused_names

    def test_class_def(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("class Foo:\n    pass\nclass Bar:\n    pass\nFoo()\n")
        result = analyze_file(str(f))
        unused_names = [d["name"] for d in result["unused_defs"]]
        assert "Bar" in unused_names

    def test_detect_unreachable_code(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("def foo():\n    return 1\n    print('unreachable')\n")
        result = analyze_file(str(f))
        assert len(result["unreachable"]) > 0

    def test_if_unreachable(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("if True:\n    return\n    print('a')\nelse:\n    break\n    print('b')\n")
        result = analyze_file(str(f))
        assert len(result["unreachable"]) == 2

    def test_for_unreachable(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("for i in range(1):\n    continue\n    print('a')\n")
        result = analyze_file(str(f))
        assert len(result["unreachable"]) >= 1

    def test_while_unreachable(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("while True:\n    break\n    print('a')\n")
        result = analyze_file(str(f))
        assert len(result["unreachable"]) >= 1

    def test_syntax_error_handling(self, tmp_path):
        f = tmp_path / "bad.py"
        f.write_text("def foo(\n")
        result = analyze_file(str(f))
        assert len(result["errors"]) > 0
        assert "SyntaxError" in result["errors"][0]

    def test_clean_file(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text("import os\npath = os.getcwd()\nprint(path)\n")
        result = analyze_file(str(f))
        assert len(result["unused_imports"]) == 0
        assert len(result["errors"]) == 0

    def test_nonexistent_file(self):
        result = analyze_file("/nonexistent/file.py")
        assert len(result["errors"]) > 0


class TestScanDirectory:
    def test_scan_with_findings(self, tmp_path):
        f = tmp_path / "module.py"
        f.write_text("import os\nimport sys\nprint('hi')\n")
        results = scan_directory(str(tmp_path))
        assert len(results) > 0

    def test_scan_empty_dir(self, tmp_path):
        results = scan_directory(str(tmp_path))
        assert len(results) == 0

    def test_ignores_pycache(self, tmp_path):
        cache_dir = tmp_path / "__pycache__"
        cache_dir.mkdir()
        f = cache_dir / "cached.py"
        f.write_text("import os\n")
        results = scan_directory(str(tmp_path))
        assert len(results) == 0


class TestFormatReport:
    def test_clean_report(self):
        report = format_report({})
        assert "No dead code found" in report

    def test_report_with_findings(self, tmp_path):
        results = {
            "/test/file.py": {
                "unused_imports": [{"name": "os", "alias": "os", "line": 1}, {"name": "sys", "alias": "s", "line": 2}],
                "unused_defs": [{"name": "foo", "kind": "function", "line": 3}],
                "unreachable": [{"description": "Code after return", "line": 4}],
                "errors": ["Some error"],
            }
        }
        report = format_report(results)
        assert "Unused import" in report
        assert "os" in report
        assert "s'" in report
        assert "Unused function:" in report
        assert "Unreachable code: Code after return" in report
        assert "Some error" in report
        assert "Parse errors: 1" in report


class TestMainExecution:
    @patch("sys.argv", ["main.py"])
    def test_main_no_args(self, capsys):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "Usage" in captured.out

    @patch("sys.argv", ["main.py", "invalid_dir_123"])
    def test_main_invalid_dir(self, capsys):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "not a valid directory" in captured.out

    @patch("sys.argv", ["main.py", "."])
    def test_main_valid(self, capsys):
        main()
        captured = capsys.readouterr()
        assert "Dead Code Removal Report" in captured.out
