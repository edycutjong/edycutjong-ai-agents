"""Tests for Lorem Ipsum Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate, generate_words, generate_sentences, generate_paragraphs, format_result_markdown, WORDS

def test_words(): text = generate_words(10); assert len(text.split()) == 10
def test_starts_lorem(): text = generate_words(5); assert text.startswith("lorem")
def test_no_lorem(): text = generate_words(5, start_with_lorem=False); assert len(text.split()) == 5
def test_sentences(): text = generate_sentences(3); assert text.count(".") >= 3
def test_sentence_cap(): text = generate_sentences(1); assert text[0].isupper()
def test_paragraphs(): text = generate_paragraphs(2); assert "\n\n" in text
def test_gen_words(): r = generate(words=20); assert r.word_count == 20
def test_gen_sentences(): r = generate(sentences=3); assert r.sentence_count == 3
def test_gen_paragraphs(): r = generate(paragraphs=2); assert r.paragraph_count == 2
def test_gen_default(): r = generate(); assert r.paragraph_count == 3
def test_char_count(): r = generate(words=10); assert r.char_count > 0
def test_empty_words(): text = generate_words(0); assert text == ""
def test_word_list(): assert len(WORDS) >= 50
def test_format(): md = format_result_markdown(generate(words=10)); assert "Lorem Ipsum" in md
def test_to_dict(): d = generate(words=10).to_dict(); assert "words" in d
