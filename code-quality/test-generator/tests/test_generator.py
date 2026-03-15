"""Tests for the test generator agent."""
import os
import tempfile
import pytest

from agent.generator import TestGenerator, TestResult
from agent.analyzer import CoverageAnalyzer, CoverageReport


SAMPLE_PYTHON = '''
def add(a, b):
    """Add two numbers."""
    return a + b

def greet(name):
    """Return greeting string."""
    return f"Hello, {name}!"

class Calculator:
    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
'''

SAMPLE_JS = '''
export function add(a, b) {
  return a + b;
}

export const multiply = (a, b) => a * b;
'''


class TestTestGenerator:
    """Tests for TestGenerator class."""

    def test_init_default_framework(self):
        gen = TestGenerator()
        assert gen.framework == "pytest"

    def test_init_custom_framework(self):
        gen = TestGenerator(framework="jest")
        assert gen.framework == "jest"

    def test_generate_python(self):
        gen = TestGenerator(framework="pytest")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(SAMPLE_PYTHON)
            f.flush()
            result = gen.generate(f.name)
        os.unlink(f.name)

        assert isinstance(result, TestResult)
        assert result.framework == "pytest"
        assert result.function_count >= 2
        assert "test_add" in result.test_code
        assert "test_greet" in result.test_code

    def test_generate_python_with_edge_cases(self):
        gen = TestGenerator(framework="pytest")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(SAMPLE_PYTHON)
            f.flush()
            result = gen.generate(f.name, include_edge_cases=True)
        os.unlink(f.name)

        assert "edge" in result.test_code.lower()

    def test_generate_js(self):
        gen = TestGenerator(framework="jest")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(SAMPLE_JS)
            f.flush()
            result = gen.generate(f.name)
        os.unlink(f.name)

        assert result.framework == "jest"
        assert "describe" in result.test_code

    def test_scan_directory(self):
        gen = TestGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create sample files
            with open(os.path.join(tmpdir, "utils.py"), "w") as f:
                f.write("def foo(): pass")
            with open(os.path.join(tmpdir, "test_utils.py"), "w") as f:
                f.write("def test_foo(): pass")
            with open(os.path.join(tmpdir, "readme.txt"), "w") as f:
                f.write("not a python file")

            sources = gen.scan_directory(tmpdir)
            basenames = [os.path.basename(s) for s in sources]
            assert "utils.py" in basenames
            assert "test_utils.py" not in basenames
            assert "readme.txt" not in basenames

    def test_result_preview(self):
        result = TestResult(
            source_path="/tmp/test.py",
            test_code="line1\nline2\nline3",
            framework="pytest",
        )
        preview = result.preview()
        assert "test.py" in preview

    def test_result_save(self):
        result = TestResult(
            source_path="/tmp/utils.py",
            test_code="# generated test code",
            framework="pytest",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = result.save(tmpdir)
            assert os.path.exists(path)
            assert "test_utils.py" in path


class TestCoverageAnalyzer:
    """Tests for CoverageAnalyzer class."""

    def test_analyze_file(self):
        analyzer = CoverageAnalyzer()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(SAMPLE_PYTHON)
            f.flush()
            report = analyzer.analyze(f.name)
        os.unlink(f.name)

        assert isinstance(report, CoverageReport)
        assert report.total_functions >= 2

    def test_report_to_dict(self):
        report = CoverageReport(total_functions=10, tested_functions=7, untested_functions=3, coverage_percent=70.0)
        d = report.to_dict()
        assert d["total_functions"] == 10
        assert d["coverage_percent"] == 70.0

    def test_report_to_markdown(self):
        report = CoverageReport(total_functions=5, tested_functions=3, untested_functions=2, coverage_percent=60.0)
        md = report.to_markdown()
        assert "Coverage Analysis Report" in md
        assert "60.0%" in md
