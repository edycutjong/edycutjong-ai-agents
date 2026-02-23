import pytest
from agent.analysis import analyze_text, interpret_flesch_score

def test_analyze_text_empty():
    result = analyze_text("")
    assert result["flesch_reading_ease"] == 0
    assert result["word_count"] == 0

def test_analyze_text_basic():
    text = "The cat sat on the mat. It was a sunny day."
    result = analyze_text(text)
    assert result["word_count"] > 0
    assert result["sentence_count"] == 2
    assert "flesch_reading_ease" in result

def test_interpret_flesch_score():
    assert interpret_flesch_score(95) == "Very Easy"
    assert interpret_flesch_score(65) == "Standard"
    assert interpret_flesch_score(10) == "Very Difficult"
