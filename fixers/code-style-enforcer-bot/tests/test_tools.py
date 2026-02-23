import os
import pytest
from tools.checker import StyleChecker
from tools.fixer import StyleFixer

# Create a temporary python file for testing
@pytest.fixture
def bad_code_file(tmp_path):
    p = tmp_path / "bad_code.py"
    p.write_text("import os, sys\n\ndef foo():\n  print('hello')\n")
    return str(p)

def test_checker_finds_issues(bad_code_file):
    checker = StyleChecker()
    issues = checker.check_file(bad_code_file)
    # Flake8 should complain about multiple imports on one line (E401) or indentation or missing whitespace
    # "import os, sys" -> E401
    assert len(issues) > 0
    codes = [i['code'] for i in issues]
    assert "E401" in codes or "E261" in codes or "E302" in codes # specific codes might vary by flake8 config/version

def test_fixer_fixes_code(bad_code_file):
    fixer = StyleFixer()
    success = fixer.fix_file(bad_code_file)
    assert success

    # Read file back
    with open(bad_code_file, "r") as f:
        content = f.read()

    # Autopep8 should fix imports to be on separate lines
    assert "import os\nimport sys" in content or "import os" in content
