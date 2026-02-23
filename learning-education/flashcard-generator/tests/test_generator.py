"""Tests for Flashcard Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import Flashcard, Deck, generate_from_topic, generate_from_terms, generate_from_text, review_session, export_anki, format_deck_markdown

def test_flashcard_accuracy():
    f = Flashcard(front="Q", back="A", times_reviewed=10, times_correct=7)
    assert f.accuracy == 70.0

def test_flashcard_accuracy_zero():
    f = Flashcard(front="Q", back="A")
    assert f.accuracy == 0.0

def test_flashcard_to_dict():
    f = Flashcard(front="Q", back="A")
    d = f.to_dict()
    assert d["front"] == "Q"

def test_deck_size():
    d = Deck(name="Test", cards=[Flashcard(front="Q", back="A")])
    assert d.size == 1

def test_deck_add():
    d = Deck(name="Test")
    d.add(Flashcard(front="Q", back="A"))
    assert d.size == 1

def test_generate_python():
    d = generate_from_topic("python", count=3)
    assert d.size == 3
    assert "Python" in d.name

def test_generate_javascript():
    d = generate_from_topic("javascript", count=2)
    assert d.size == 2

def test_generate_unknown():
    d = generate_from_topic("unknown-topic", count=3)
    assert d.size >= 1

def test_generate_capped():
    d = generate_from_topic("git", count=100)
    assert d.size <= 12  # total cards in bank

def test_generate_from_terms():
    d = generate_from_terms({"API": "Application Programming Interface", "REST": "Representational State Transfer"})
    assert d.size == 2

def test_generate_from_text():
    text = "API: Application Programming Interface\nREST - Representational State Transfer"
    d = generate_from_text(text)
    assert d.size == 2

def test_review_session():
    d = generate_from_topic("python", count=3)
    session = review_session(d, shuffle=False)
    assert len(session) == 3
    assert "front" in session[0]

def test_export_anki():
    d = generate_from_topic("python", count=2)
    tsv = export_anki(d)
    lines = tsv.strip().split("\n")
    assert len(lines) == 2
    assert "\t" in lines[0]

def test_format_markdown():
    d = generate_from_topic("python", count=2)
    md = format_deck_markdown(d)
    assert "Card 1" in md

def test_deck_to_dict():
    d = generate_from_topic("python", count=2)
    data = d.to_dict()
    assert "cards" in data
    assert data["size"] == 2
