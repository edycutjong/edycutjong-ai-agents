"""Tests for Word Counter."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.counter import count_words, keyword_density, flesch_reading_ease, compare_texts, format_result_markdown, STOP_WORDS

TEXT = "Hello world. This is a test sentence. Another sentence here."
PARA = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

def test_words(): r = count_words(TEXT); assert r.words == 10
def test_chars(): r = count_words(TEXT); assert r.characters == len(TEXT)
def test_sentences(): r = count_words(TEXT); assert r.sentences == 3
def test_unique(): r = count_words(TEXT); assert r.unique_words <= r.words
def test_reading_time(): r = count_words("word " * 200); assert abs(r.reading_time_min - 1.0) < 0.1
def test_paragraphs(): r = count_words(PARA); assert r.paragraphs == 3
def test_top_words(): r = count_words("apple apple banana"); assert r.top_words[0][0] == "apple"
def test_stop_words(): assert "the" in STOP_WORDS
def test_empty(): r = count_words(""); assert r.words == 0
def test_avg_length(): r = count_words("hello world"); assert r.avg_word_length > 0
def test_keyword_density(): d = keyword_density("test test other", "test"); assert abs(d - 66.67) < 1
def test_density_zero(): assert keyword_density("hello world", "missing") == 0
def test_flesch(): score = flesch_reading_ease("The cat sat. The dog ran."); assert isinstance(score, float)
def test_compare(): d = compare_texts("hello", "hello world"); assert d["words_diff"] == 1
def test_format(): md = format_result_markdown(count_words(TEXT)); assert "Word Count" in md
def test_to_dict(): d = count_words(TEXT).to_dict(); assert "words" in d
