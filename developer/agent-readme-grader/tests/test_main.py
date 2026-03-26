import pytest
from unittest.mock import patch
from main import run, grade_readme, format_report, main


def test_run():
    assert "README Grader" in run("test")


def test_perfect_readme():
    content = """# My Project
## About
A great project.
## Installation
pip install myproject
## Usage
```python
import myproject
```
## API
Reference docs here.
## Contributing
See CONTRIBUTING.md
## License
MIT
"""
    result = grade_readme(content)
    assert result["score"] >= 7


def test_minimal_readme():
    result = grade_readme("# Hello\nA project.")
    assert result["score"] < 5
    assert len(result["missing"]) > 3


def test_empty_readme():
    result = grade_readme("")
    assert result["grade"] in ("D", "F")


def test_long_readme():
    content = "word " * 501
    result = grade_readme(content)
    assert result["score"] >= 1


def test_format_report():
    result = {"score": 7.5, "grade": "B", "word_count": 300,
              "found": ["Title"], "missing": [{"section": "License", "weight": 1}],
              "raw_score": 5, "max_score": 7.5}
    report = format_report(result)
    assert "7.5" in report
    assert "License" in report


def test_format_no_missing():
    res = {"score": 10, "grade": "A", "word_count": 600, "found": ["All"], "missing": [], "raw_score": 10, "max_score": 10}
    assert "Missing" not in format_report(res)


def test_format_no_found():
    res = {"score": 0, "grade": "F", "word_count": 0, "found": [], "missing": [{"section": "A", "weight": 1}], "raw_score": 0, "max_score": 10}
    assert "Present:" not in format_report(res)


@patch("sys.argv", ["main.py"])
def test_main_no_args(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out


def test_main_success(capsys, tmp_path):
    p = tmp_path / "README.md"
    p.write_text("# Title\nword " * 600)
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()
    assert "README Score" in captured.out
