from main import run, grade_readme, format_report


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


def test_format_report():
    result = {"score": 7.5, "grade": "B", "word_count": 300,
              "found": ["Title"], "missing": [{"section": "License", "weight": 1}],
              "raw_score": 5, "max_score": 7.5}
    report = format_report(result)
    assert "7.5" in report
    assert "License" in report
