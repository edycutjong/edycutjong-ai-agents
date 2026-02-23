"""Tests for Training Data Generator."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import (
    TrainingExample, generate_from_template, generate_variations,
    validate_dataset, export_dataset, format_stats_markdown, TEMPLATES,
)

# --- TrainingExample ---
def test_to_alpaca():
    ex = TrainingExample(instruction="Test", input="data", output="result")
    d = ex.to_alpaca()
    assert d["instruction"] == "Test"
    assert d["output"] == "result"

def test_to_chat():
    ex = TrainingExample(instruction="Hello", output="Hi")
    msgs = ex.to_chat()["messages"]
    assert len(msgs) == 3
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert msgs[2]["role"] == "assistant"

def test_to_completion():
    ex = TrainingExample(instruction="Prompt", output="Response")
    d = ex.to_completion()
    assert d["prompt"] == "Prompt"
    assert d["completion"] == "Response"

# --- Generation ---
def test_generate_qa():
    examples = generate_from_template("qa", {"topic": "Python", "definition": "a programming language"}, count=3)
    assert len(examples) == 3
    assert all("Python" in e.instruction or "Python" in e.input or "Python" in e.output for e in examples)

def test_generate_classification():
    examples = generate_from_template("classification", {"text": "Great product!", "label": "positive"}, count=2)
    assert len(examples) == 2

def test_generate_unknown_category():
    examples = generate_from_template("nonexistent", {}, count=5)
    assert len(examples) == 0

def test_generate_code():
    examples = generate_from_template("code", {"language": "python", "task": "sort a list", "code": "sorted(l)", "fixed_code": "sorted(l)"}, count=2)
    assert len(examples) == 2

# --- Variations ---
def test_generate_variations():
    ex = TrainingExample(instruction="Explain gravity", output="Gravity is a force")
    variations = generate_variations(ex, count=5)
    assert len(variations) == 5
    assert all(v.output == ex.output for v in variations)

def test_variations_are_different():
    ex = TrainingExample(instruction="What is AI?", output="AI is...")
    variations = generate_variations(ex, count=10)
    unique = set(v.instruction for v in variations)
    assert len(unique) > 1  # at least some should differ

# --- Validation ---
def test_validate_good_dataset():
    examples = [TrainingExample(instruction=f"Task number {i}", output=f"Result {i}") for i in range(5)]
    stats = validate_dataset(examples)
    assert stats["total"] == 5
    assert stats["quality_score"] > 50

def test_validate_empty_output():
    examples = [TrainingExample(instruction="Do something", output="")]
    stats = validate_dataset(examples)
    assert len(stats["issues"]) > 0

def test_validate_duplicate():
    examples = [
        TrainingExample(instruction="Same task", output="Result 1"),
        TrainingExample(instruction="Same task", output="Result 2"),
    ]
    stats = validate_dataset(examples)
    assert any("duplicate" in i for i in stats["issues"])

def test_validate_short_instruction():
    examples = [TrainingExample(instruction="Hi", output="Hello")]
    stats = validate_dataset(examples)
    assert any("short" in i for i in stats["issues"])

# --- Export ---
def test_export_alpaca():
    examples = [TrainingExample(instruction="Test", output="Out")]
    data = json.loads(export_dataset(examples, "alpaca"))
    assert isinstance(data, list)
    assert data[0]["instruction"] == "Test"

def test_export_chat():
    examples = [TrainingExample(instruction="Test", output="Out")]
    data = json.loads(export_dataset(examples, "chat"))
    assert "messages" in data[0]

def test_export_jsonl():
    examples = [TrainingExample(instruction="Test", output="Out"), TrainingExample(instruction="T2", output="O2")]
    lines = export_dataset(examples, "jsonl").strip().split("\n")
    assert len(lines) == 2

def test_export_completion():
    examples = [TrainingExample(instruction="Test", output="Out")]
    line = export_dataset(examples, "completion").strip()
    d = json.loads(line)
    assert "prompt" in d and "completion" in d

# --- Stats Formatting ---
def test_format_stats():
    examples = [TrainingExample(instruction="Task 1", output="Out", category="qa")]
    stats = validate_dataset(examples)
    md = format_stats_markdown(stats)
    assert "Training Data" in md

# --- Templates ---
def test_templates_exist():
    assert len(TEMPLATES) >= 6
    assert "qa" in TEMPLATES
    assert "code" in TEMPLATES
