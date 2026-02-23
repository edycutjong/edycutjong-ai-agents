"""Tests for Math Expression Parser."""
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.parser import evaluate, evaluate_batch, simplify_fraction, format_result_markdown

def test_add(): r = evaluate("2 + 3"); assert r.result == 5
def test_sub(): r = evaluate("10 - 4"); assert r.result == 6
def test_mul(): r = evaluate("3 * 4"); assert r.result == 12
def test_div(): r = evaluate("10 / 4"); assert abs(r.result - 2.5) < 0.01
def test_pow(): r = evaluate("2 ** 8"); assert r.result == 256
def test_caret(): r = evaluate("2^10"); assert r.result == 1024
def test_sqrt(): r = evaluate("sqrt(16)"); assert r.result == 4
def test_sin(): r = evaluate("sin(0)"); assert r.result == 0
def test_pi(): r = evaluate("pi"); assert abs(r.result - math.pi) < 0.001
def test_nested(): r = evaluate("(2 + 3) * 4"); assert r.result == 20
def test_variable(): r = evaluate("x * 2", {"x": 5}); assert r.result == 10
def test_multi_var(): r = evaluate("a + b", {"a": 3, "b": 7}); assert r.result == 10
def test_div_zero(): r = evaluate("1 / 0"); assert not r.is_valid
def test_invalid(): r = evaluate("???"); assert not r.is_valid
def test_unsafe(): r = evaluate("__import__('os')"); assert not r.is_valid
def test_batch(): results = evaluate_batch(["1+1", "2*3"]); assert results[0].result == 2 and results[1].result == 6
def test_gcd(): n, d = simplify_fraction(6, 4); assert n == 3 and d == 2
def test_format(): md = format_result_markdown(evaluate("2+2")); assert "Math Parser" in md
def test_to_dict(): d = evaluate("1+1").to_dict(); assert "result" in d
