"""Tests for Quiz Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import Question, Quiz, generate_quiz, grade_quiz, format_quiz_markdown, format_results_markdown, QUESTION_BANK

def test_question_correct_answer():
    q = Question(text="?", options=["A", "B", "C"], correct=1)
    assert q.correct_answer == "B"

def test_question_to_dict():
    q = Question(text="?", options=["A"], correct=0)
    assert q.to_dict()["text"] == "?"

def test_generate_python():
    quiz = generate_quiz("python", count=3)
    assert len(quiz.questions) == 3
    assert quiz.title == "Python Quiz"

def test_generate_javascript():
    quiz = generate_quiz("javascript", count=2)
    assert len(quiz.questions) == 2

def test_generate_unknown_topic():
    quiz = generate_quiz("unknown-topic", count=3)
    assert len(quiz.questions) >= 1  # falls back to all questions

def test_generate_capped():
    quiz = generate_quiz("python", count=100)
    assert len(quiz.questions) <= len(QUESTION_BANK["python"])

def test_grade_all_correct():
    quiz = generate_quiz("python", count=3)
    answers = [q.correct for q in quiz.questions]
    result = grade_quiz(quiz, answers)
    assert result.score == 100.0
    assert result.passed

def test_grade_all_wrong():
    quiz = generate_quiz("python", count=3)
    answers = [(q.correct + 1) % len(q.options) for q in quiz.questions]
    result = grade_quiz(quiz, answers)
    assert result.score == 0.0
    assert not result.passed

def test_grade_partial():
    quiz = Quiz(title="Test", questions=[
        Question(text="Q1", options=["A","B"], correct=0),
        Question(text="Q2", options=["A","B"], correct=1),
    ])
    result = grade_quiz(quiz, [0, 0])  # 1 correct, 1 wrong
    assert result.correct == 1
    assert result.wrong == 1
    assert result.score == 50.0

def test_grade_missing_answers():
    quiz = generate_quiz("python", count=3)
    result = grade_quiz(quiz, [0])
    assert result.total == 3

def test_quiz_to_dict():
    quiz = generate_quiz("python", count=2)
    d = quiz.to_dict()
    assert "questions" in d
    assert d["total"] == 2

def test_format_quiz():
    quiz = generate_quiz("python", count=2)
    md = format_quiz_markdown(quiz)
    assert "Quiz" in md
    assert "Q1." in md

def test_format_results():
    quiz = generate_quiz("python", count=2)
    result = grade_quiz(quiz, [q.correct for q in quiz.questions])
    md = format_results_markdown(result)
    assert "Results" in md
    assert "100.0%" in md

def test_passing_score():
    quiz = Quiz(title="T", passing_score=50, questions=[Question(text="Q", options=["A","B"], correct=0)])
    result = grade_quiz(quiz, [0])
    assert result.passed

def test_bank_has_topics():
    assert "python" in QUESTION_BANK
    assert "javascript" in QUESTION_BANK
    assert "general-cs" in QUESTION_BANK
