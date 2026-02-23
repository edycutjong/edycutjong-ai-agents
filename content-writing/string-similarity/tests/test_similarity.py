"""Tests for String Similarity."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.similarity import levenshtein, jaro_winkler, similarity_ratio, compare, closest_match, format_result_markdown

def test_same(): assert levenshtein("abc", "abc") == 0
def test_insert(): assert levenshtein("abc", "abcd") == 1
def test_delete(): assert levenshtein("abcd", "abc") == 1
def test_replace(): assert levenshtein("abc", "axc") == 1
def test_empty(): assert levenshtein("", "abc") == 3
def test_ratio_same(): assert similarity_ratio("hello", "hello") == 1.0
def test_ratio_diff(): assert 0 < similarity_ratio("hello", "world") < 1
def test_jaro_same(): assert jaro_winkler("abc", "abc") == 1.0
def test_jaro_diff(): assert 0 < jaro_winkler("hello", "hallo") < 1
def test_jaro_empty(): assert jaro_winkler("", "abc") == 0.0
def test_compare_lev(): r = compare("cat", "bat"); assert r.distance == 1
def test_compare_jw(): r = compare("cat", "cat", "jaro_winkler"); assert r.ratio == 1.0
def test_closest(): assert closest_match("cat", ["bat", "dog", "car"]) == "bat"
def test_closest_empty(): assert closest_match("x", []) == ""
def test_format(): md = format_result_markdown(compare("a", "b")); assert "Similarity" in md
def test_to_dict(): d = compare("a", "b").to_dict(); assert "ratio" in d
