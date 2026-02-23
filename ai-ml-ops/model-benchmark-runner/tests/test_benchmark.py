"""Tests for Model Benchmark Runner."""
import sys, os, tempfile, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.benchmark import (
    BenchmarkCase, ModelResult, run_benchmark, evaluate_output,
    score_exact_match, score_contains, score_length_ratio,
    score_keyword_coverage, score_format_quality, format_report_markdown,
    BenchmarkStorage,
)

CASES = [
    BenchmarkCase(prompt="What is 2+2?", expected="4"),
    BenchmarkCase(prompt="Capital of France?", expected="Paris"),
    BenchmarkCase(prompt="List 3 colors", expected="red blue green"),
]
OUTPUTS = {
    "model-a": ["4", "Paris", "red, blue, and green"],
    "model-b": ["The answer is 4.", "The capital is Paris.", "1. Red\n2. Blue\n3. Green"],
    "model-c": ["22", "London", "color"],
}

# --- Scoring ---
def test_exact_match_true():
    assert score_exact_match("4", "4") == 1.0

def test_exact_match_false():
    assert score_exact_match("The answer is 4", "4") == 0.0

def test_contains_true():
    assert score_contains("The capital is Paris.", "Paris") == 1.0

def test_contains_false():
    assert score_contains("London", "Paris") == 0.0

def test_length_ratio_similar():
    s = score_length_ratio("hello world", "hello there")
    assert s > 0.8

def test_keyword_coverage_full():
    assert score_keyword_coverage("red blue green", "red blue green") == 1.0

def test_keyword_coverage_partial():
    s = score_keyword_coverage("red and yellow", "red blue green")
    assert 0.0 < s < 1.0

def test_format_quality_structured():
    s = score_format_quality("# Title\n\n- Item 1\n- Item 2\n- Item 3\n\nConclusion.")
    assert s >= 0.8

def test_format_quality_plain():
    s = score_format_quality("ok")
    assert s < 0.8

def test_evaluate_output():
    scores = evaluate_output("Paris", "Paris")
    assert "exact_match" in scores
    assert "average" in scores
    assert scores["exact_match"] == 1.0

# --- Benchmark ---
def test_run_benchmark():
    report = run_benchmark(CASES, OUTPUTS)
    assert len(report.models) == 3
    assert len(report.results) == 9  # 3 cases x 3 models

def test_winner():
    report = run_benchmark(CASES, OUTPUTS)
    assert report.summary.get("winner") in ["model-a", "model-b"]

def test_scores_bounded():
    report = run_benchmark(CASES, OUTPUTS)
    for r in report.results:
        assert 0 <= r.scores.get("average", 0) <= 1

def test_report_to_dict():
    report = run_benchmark(CASES, OUTPUTS)
    d = report.to_dict()
    assert "models" in d
    assert "results" in d

# --- Formatting ---
def test_format_markdown():
    report = run_benchmark(CASES, OUTPUTS)
    md = format_report_markdown(report)
    assert "Benchmark Report" in md
    assert "Winner" in md

# --- Storage ---
def test_storage(tmp_path):
    path = str(tmp_path / "bench.json")
    s = BenchmarkStorage(filepath=path)
    report = run_benchmark(CASES, OUTPUTS)
    s.save(report)
    assert len(s.get_all()) == 1

# --- Edge ---
def test_empty_benchmark():
    report = run_benchmark([], {})
    assert len(report.results) == 0
