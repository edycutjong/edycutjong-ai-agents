"""Tests for Gitignore Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate, get_languages, get_template, merge_gitignores, format_result_markdown, TEMPLATES

def test_python(): r = generate(["python"]); assert "__pycache__/" in r.content
def test_node(): r = generate(["node"]); assert "node_modules/" in r.content
def test_java(): r = generate(["java"]); assert "*.class" in r.content
def test_general(): r = generate(["python"]); assert ".DS_Store" in r.content
def test_multi(): r = generate(["python", "node"]); assert "__pycache__/" in r.content and "node_modules/" in r.content
def test_custom(): r = generate(["python"], custom=["*.db"]); assert "*.db" in r.content
def test_pattern_count(): r = generate(["python"]); assert r.pattern_count >= 10
def test_languages(): langs = get_languages(); assert "python" in langs and "node" in langs
def test_template(): t = get_template("python"); assert "__pycache__/" in t
def test_empty_template(): t = get_template("nonexistent"); assert t == []
def test_merge_new(): result = merge_gitignores("*.log\n", ["*.tmp"]); assert "*.tmp" in result
def test_merge_existing(): result = merge_gitignores("*.log\n", ["*.log"]); assert result.count("*.log") == 1
def test_go(): r = generate(["go"]); assert "vendor/" in r.content
def test_rust(): r = generate(["rust"]); assert "target/" in r.content
def test_templates(): assert len(TEMPLATES) >= 6
def test_format(): md = format_result_markdown(generate(["python"])); assert "Gitignore Generator" in md
def test_to_dict(): d = generate(["python"]).to_dict(); assert "patterns" in d
