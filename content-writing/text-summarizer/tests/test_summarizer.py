"""Tests for Text Summarizer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.summarizer import summarize, split_sentences, extract_keywords, score_sentence, format_result_markdown

ARTICLE = """Machine learning is a subset of artificial intelligence that enables systems to learn from data. It has transformed industries ranging from healthcare to finance. Deep learning, a subfield of machine learning, uses neural networks with multiple layers. These networks can process vast amounts of data and identify complex patterns. Natural language processing is another key area that benefits from machine learning. Companies like Google and OpenAI have made significant advances in this field. The future of machine learning looks promising with continued research and innovation."""

def test_split_sentences():
    s = split_sentences(ARTICLE)
    assert len(s) >= 5

def test_summarize_shorter():
    r = summarize(ARTICLE)
    assert r.summary_length < r.original_length

def test_summarize_ratio():
    r = summarize(ARTICLE, ratio=0.3)
    assert r.summary_sentences <= r.sentence_count

def test_compression():
    r = summarize(ARTICLE)
    assert 0 < r.compression_ratio < 1

def test_keywords():
    kw = extract_keywords(ARTICLE)
    assert "learning" in kw or "machine" in kw

def test_keywords_no_stop():
    kw = extract_keywords("the the the is is are are machine learning")
    assert "the" not in kw and "is" not in kw

def test_score_first():
    s1 = score_sentence("machine learning is great", ["machine", "learning"], 0, 10)
    s2 = score_sentence("machine learning is great", ["machine", "learning"], 5, 10)
    assert s1 > s2

def test_max_sentences():
    r = summarize(ARTICLE, max_sentences=2)
    assert r.summary_sentences <= 2

def test_short_text():
    r = summarize("Short text.")
    assert r.summary_length > 0

def test_original_length():
    r = summarize(ARTICLE)
    assert r.original_length == len(ARTICLE)

def test_sentence_count():
    r = summarize(ARTICLE)
    assert r.sentence_count >= 5

def test_format():
    r = summarize(ARTICLE)
    md = format_result_markdown(r)
    assert "Summary" in md and "Compression" in md

def test_to_dict():
    r = summarize(ARTICLE)
    d = r.to_dict()
    assert "compression_ratio" in d

def test_keywords_in_result():
    r = summarize(ARTICLE)
    assert len(r.keywords) > 0
