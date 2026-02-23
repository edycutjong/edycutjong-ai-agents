"""Tests for SQL Formatter."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.formatter import format_sql, extract_columns, detect_sql_injection, format_result_markdown, KEYWORDS

def test_select(): r = format_sql("SELECT * FROM users"); assert r.query_type == "SELECT"
def test_insert(): r = format_sql("INSERT INTO users VALUES (1)"); assert r.query_type == "INSERT"
def test_update(): r = format_sql("UPDATE users SET name='x'"); assert r.query_type == "UPDATE"
def test_delete(): r = format_sql("DELETE FROM users"); assert r.query_type == "DELETE"
def test_tables(): r = format_sql("SELECT * FROM users JOIN orders ON users.id = orders.uid"); assert "users" in r.tables
def test_multi_table(): r = format_sql("SELECT * FROM users JOIN orders ON 1=1"); assert len(r.tables) >= 2
def test_keywords(): r = format_sql("SELECT name FROM users WHERE id = 1"); assert r.keyword_count >= 3
def test_formatted(): r = format_sql("SELECT name FROM users WHERE id = 1"); assert "\n" in r.formatted
def test_empty(): r = format_sql(""); assert not r.is_valid
def test_columns(): cols = extract_columns("SELECT name, age FROM users"); assert "name" in cols
def test_columns_alias(): cols = extract_columns("SELECT u.name AS n FROM users u"); assert "n" in cols
def test_injection_or(): risks = detect_sql_injection("SELECT * FROM users WHERE name='' OR '1'='1'"); assert len(risks) >= 1
def test_injection_drop(): risks = detect_sql_injection("SELECT 1; DROP TABLE users"); assert len(risks) >= 1
def test_injection_union(): risks = detect_sql_injection("SELECT 1 UNION SELECT password FROM admin"); assert len(risks) >= 1
def test_no_injection(): risks = detect_sql_injection("SELECT * FROM users WHERE id = 1"); assert len(risks) == 0
def test_keyword_set(): assert len(KEYWORDS) >= 30
def test_format(): md = format_result_markdown(format_sql("SELECT 1")); assert "SQL Formatter" in md
def test_to_dict(): d = format_sql("SELECT 1").to_dict(); assert "query_type" in d
