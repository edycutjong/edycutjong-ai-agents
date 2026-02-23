"""Tests for SQL Query Optimizer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.optimizer import analyze_query, detect_query_type, extract_tables, format_analysis_markdown

def test_detect_select(): assert detect_query_type("SELECT * FROM users") == "SELECT"
def test_detect_insert(): assert detect_query_type("INSERT INTO users VALUES (1)") == "INSERT"
def test_detect_update(): assert detect_query_type("UPDATE users SET name='x'") == "UPDATE"
def test_detect_delete(): assert detect_query_type("DELETE FROM users") == "DELETE"

def test_extract_tables():
    t = extract_tables("SELECT * FROM users JOIN orders ON users.id = orders.user_id")
    assert "users" in t and "orders" in t

def test_select_star():
    a = analyze_query("SELECT * FROM users")
    assert a.has_select_star and a.score < 100

def test_no_where():
    a = analyze_query("SELECT id FROM users")
    assert not a.has_where and any("WHERE" in i for i in a.issues)

def test_with_where():
    a = analyze_query("SELECT id FROM users WHERE id = 1")
    assert a.has_where

def test_subquery():
    a = analyze_query("SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)")
    assert a.has_subquery

def test_leading_wildcard():
    a = analyze_query("SELECT * FROM users WHERE name LIKE '%john%'")
    assert any("wildcard" in i for i in a.issues)

def test_order_no_limit():
    a = analyze_query("SELECT id FROM users WHERE id > 0 ORDER BY name")
    assert any("LIMIT" in s for s in a.suggestions)

def test_order_with_limit():
    a = analyze_query("SELECT id FROM users ORDER BY name LIMIT 10")
    assert not any("LIMIT" in i for i in a.issues)

def test_distinct():
    a = analyze_query("SELECT DISTINCT name FROM users WHERE id > 0")
    assert any("DISTINCT" in i for i in a.issues)

def test_many_joins():
    a = analyze_query("SELECT * FROM a JOIN b ON a.id=b.id JOIN c ON b.id=c.id JOIN d ON c.id=d.id JOIN e ON d.id=e.id WHERE a.id=1")
    assert any("JOIN" in i for i in a.issues)

def test_good_query():
    a = analyze_query("SELECT id, name FROM users WHERE status = 'active' LIMIT 10")
    assert a.score >= 80

def test_score_capped():
    a = analyze_query("SELECT * FROM users")
    assert 0 <= a.score <= 100

def test_format():
    a = analyze_query("SELECT * FROM users")
    md = format_analysis_markdown(a)
    assert "SQL Analysis" in md
