"""Tests for the Dead Code Finder Agent."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import analyze_file, scan_directory, format_report


class TestAnalyzeFile:
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

    def test_detect_unused_function(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("def unused_func():\n    pass\n\ndef main():\n    pass\n\nmain()\n")
        result = analyze_file(str(f))
        unused_names = [d["name"] for d in result["unused_defs"]]
        assert "unused_func" in unused_names

    def test_detect_unreachable_code(self, tmp_path):
        f = tmp_path / "test_file.py"
        f.write_text("def foo():\n    return 1\n    print('unreachable')\n")
        result = analyze_file(str(f))
        assert len(result["unreachable"]) > 0

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
                "unused_imports": [{"name": "os", "alias": "os", "line": 1}],
                "unused_defs": [],
                "unreachable": [],
                "errors": [],
            }
        }
        report = format_report(results)
        assert "Unused import" in report
        assert "os" in report
