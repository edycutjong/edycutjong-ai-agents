from lib.reporter import format_terminal, format_json, format_markdown
import json

def test_format_terminal(capsys):
    score_data = {
        "score": 80.0,
        "criticality": 30.0,
        "blast_radius": 20.0,
        "coverage_gap": 20.0,
        "history_risk": 15.0,
        "familiarity_discount": 5.0
    }
    files = ["src/main.py"]
    
    format_terminal(score_data, files)
    
    # Check output
def test_format_terminal_no_files():
    format_terminal({}, [])
    
def test_format_terminal_medium():
    format_terminal({"score": 50.0, "criticality": 10.0, "blast_radius": 10.0, "coverage_gap": 10.0, "history_risk": 20.0, "familiarity_discount": 0.0}, ["src/main.py"])

def test_format_terminal_low():
    format_terminal({"score": 20.0, "criticality": 5.0, "blast_radius": 5.0, "coverage_gap": 5.0, "history_risk": 5.0, "familiarity_discount": 0.0}, ["src/main.py"])


def test_format_json():
    score_data = {"score": 80.0}
    output = format_json(score_data)
    assert json.loads(output) == score_data
    
def test_format_markdown():
    score_data = {
        "score": 80.0,
        "criticality": 30.0,
        "blast_radius": 20.0,
        "coverage_gap": 20.0,
        "history_risk": 15.0,
        "familiarity_discount": 5.0
    }
    
    output = format_markdown(score_data, ["src/main.py"])
    assert "## Commit Risk Analysis: 🔴 HIGH RISK (80.0/100)" in output
    
def test_format_markdown_medium():
    score_data = {
        "score": 50.0,
        "criticality": 10.0,
        "blast_radius": 10.0,
        "coverage_gap": 10.0,
        "history_risk": 20.0,
        "familiarity_discount": 0.0
    }
    output = format_markdown(score_data, ["src/main.py"])
    assert "🟡 MEDIUM RISK" in output

def test_format_markdown_low():
    score_data = {
        "score": 20.0,
        "criticality": 5.0,
        "blast_radius": 5.0,
        "coverage_gap": 5.0,
        "history_risk": 5.0,
        "familiarity_discount": 0.0
    }
    output = format_markdown(score_data, ["src/main.py"])
    assert "🟢 LOW RISK" in output
