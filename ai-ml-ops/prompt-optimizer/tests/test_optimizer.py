"""Tests for Prompt Optimizer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.optimizer import analyze_prompt, optimize_prompt, compare_prompts, format_analysis_markdown

GOOD_PROMPT = """You are an expert data scientist. Given the following CSV data, analyze it step-by-step:
1. Identify trends
2. Find outliers
3. Provide a summary

Format as a JSON object with keys: trends, outliers, summary.
Example: {"trends": ["upward sales"], "outliers": [42], "summary": "Sales grew 15%"}
Do not include any markdown formatting. Maximum 500 words."""

BAD_PROMPT = "help me"

MEDIUM_PROMPT = "Summarize this article about climate change and give me the key points."

# --- Scoring ---
def test_good_prompt_high_score():
    r = analyze_prompt(GOOD_PROMPT)
    assert r.total_score >= 70

def test_bad_prompt_low_score():
    r = analyze_prompt(BAD_PROMPT)
    assert r.total_score < 50

def test_medium_prompt_medium_score():
    r = analyze_prompt(MEDIUM_PROMPT)
    assert 30 <= r.total_score <= 80

def test_score_bounded():
    for p in [GOOD_PROMPT, BAD_PROMPT, MEDIUM_PROMPT, "", "x" * 1000]:
        r = analyze_prompt(p)
        assert 0 <= r.total_score <= 100

# --- Category Detection ---
def test_detects_role():
    r = analyze_prompt("You are an expert Python developer. Write clean code.")
    assert r.category_scores.get("role_setting", 0) >= 80

def test_detects_examples():
    r = analyze_prompt("Translate. Example: Hello -> Hola")
    assert r.category_scores.get("examples", 0) >= 80

def test_detects_constraints():
    r = analyze_prompt("Do not use jargon. Limit response to 100 words.")
    assert r.category_scores.get("constraints", 0) >= 80

def test_detects_output_structure():
    r = analyze_prompt("Return a JSON object with the results.")
    assert r.category_scores.get("output_structure", 0) >= 80

def test_detects_chain_of_thought():
    r = analyze_prompt("Think through this step-by-step and explain your reasoning.")
    assert r.category_scores.get("chain_of_thought", 0) >= 80

# --- Word/Token Count ---
def test_word_count():
    r = analyze_prompt("one two three four five")
    assert r.word_count == 5

def test_token_estimate():
    r = analyze_prompt("one two three four five")
    assert r.token_estimate > r.word_count

# --- Warnings ---
def test_short_prompt_warning():
    r = analyze_prompt("hi")
    assert any("short" in w.lower() for w in r.weaknesses)

# --- Optimization ---
def test_optimize_adds_structure():
    result = optimize_prompt("Analyze the data in the attached spreadsheet thoroughly")
    assert "step-by-step" in result.lower() or "structured" in result.lower()

def test_optimize_preserves_content():
    original = "You are an expert. Format as JSON."
    result = optimize_prompt(original)
    assert "You are an expert" in result

# --- Comparison ---
def test_compare_good_vs_bad():
    r = compare_prompts(GOOD_PROMPT, BAD_PROMPT)
    assert r["winner"] == "A"
    assert r["prompt_a_score"] > r["prompt_b_score"]

def test_compare_same():
    r = compare_prompts(GOOD_PROMPT, GOOD_PROMPT)
    assert r["winner"] == "Tie"

# --- Formatting ---
def test_format_markdown():
    r = analyze_prompt(GOOD_PROMPT)
    md = format_analysis_markdown(r)
    assert "Prompt Analysis" in md
    assert "Score" in md

def test_to_dict():
    r = analyze_prompt(GOOD_PROMPT)
    d = r.to_dict()
    assert "score" in d
    assert "suggestions" in d
