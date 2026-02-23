"""Tests for Text Diff."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.differ import diff_texts, unified_diff, word_diff, format_result_markdown

T1 = "hello\nworld\nfoo\n"
T2 = "hello\nearth\nfoo\nbar\n"

def test_identical(): r = diff_texts("abc", "abc"); assert r.added == 0 and r.removed == 0
def test_similarity_same(): r = diff_texts("abc", "abc"); assert r.similarity == 100.0
def test_similarity_diff(): r = diff_texts("abc", "xyz"); assert r.similarity < 50
def test_added(): r = diff_texts(T1, T2); assert r.added >= 1
def test_removed(): r = diff_texts(T1, T2); assert r.removed >= 1
def test_add_count(): r = diff_texts("a\n", "a\nb\n"); assert r.added == 1
def test_remove_count(): r = diff_texts("a\nb\n", "a\n"); assert r.removed == 1
def test_has_lines(): r = diff_texts(T1, T2); assert len(r.lines) > 0
def test_equal_lines(): r = diff_texts(T1, T2); assert any(l.kind == "equal" for l in r.lines)
def test_unified(): u = unified_diff(T1, T2); assert "---" in u and "+++" in u
def test_unified_additions(): u = unified_diff(T1, T2); assert "+" in u
def test_word_diff_same(): wd = word_diff("hello world", "hello world"); assert all(k == "equal" for k, _ in wd)
def test_word_added(): wd = word_diff("hello", "hello world"); assert any(k == "added" for k, _ in wd)
def test_word_removed(): wd = word_diff("hello world", "hello"); assert any(k == "removed" for k, _ in wd)
def test_empty(): r = diff_texts("", ""); assert r.similarity == 100.0
def test_to_empty(): r = diff_texts("line\n", ""); assert r.removed >= 1
def test_format(): md = format_result_markdown(diff_texts(T1, T2)); assert "Text Diff" in md
def test_to_dict(): d = diff_texts(T1, T2).to_dict(); assert "added" in d
