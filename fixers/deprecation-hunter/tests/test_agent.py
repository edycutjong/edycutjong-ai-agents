import os
import shutil
import pytest
from tools.scanner import scan_directory, get_dependencies
from tools.analyzer import DeprecationAnalyzer, DeprecationFinding
from tools.fixer import DeprecationFixer
from tools.reporter import generate_report

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "dummy_project")

@pytest.fixture
def temp_project(tmp_path):
    # Copy fixture to temp path
    target = tmp_path / "project"
    shutil.copytree(FIXTURE_PATH, target)
    return str(target)

def test_scanner(temp_project):
    files = scan_directory(temp_project)
    assert len(files) == 1
    assert files[0].endswith("main.py")

    deps = get_dependencies(temp_project)
    assert "pandas" in deps

def test_analyzer_ast(temp_project):
    analyzer = DeprecationAnalyzer(use_llm=False)
    files = scan_directory(temp_project)
    deps = get_dependencies(temp_project)

    findings = analyzer.analyze_file(files[0], deps)

    # Expect datetime.utcnow() and pandas.append()
    assert len(findings) >= 2

    codes = [f.code for f in findings]
    assert "datetime.utcnow()" in codes
    assert ".append()" in codes

def test_fixer(temp_project):
    analyzer = DeprecationAnalyzer(use_llm=False)
    fixer = DeprecationFixer()
    files = scan_directory(temp_project)
    deps = get_dependencies(temp_project)

    findings = analyzer.analyze_file(files[0], deps)

    # Filter for datetime.utcnow finding
    datetime_finding = next((f for f in findings if f.code == "datetime.utcnow()"), None)
    assert datetime_finding is not None

    # Apply fix
    success = fixer.fix_file(datetime_finding)
    assert success

    # Verify fix
    with open(files[0], "r") as f:
        content = f.read()

    assert "datetime.now(datetime.timezone.utc)" in content
    assert "datetime.utcnow()" not in content

def test_reporter(temp_project):
    findings = [
        DeprecationFinding(
            filepath="test.py",
            line_number=1,
            code="old_code()",
            message="deprecated",
            suggestion="new_code()"
        )
    ]
    report_path = os.path.join(temp_project, "report.html")
    generate_report(findings, report_path)

    assert os.path.exists(report_path)
    with open(report_path, "r") as f:
        content = f.read()
    assert "old_code()" in content
    assert "new_code()" in content
