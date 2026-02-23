"""Tests for README Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate, add_badges, add_toc, format_result_markdown

def test_title(): r = generate("MyProject"); assert "# MyProject" in r.content
def test_description(): r = generate("P", description="A tool"); assert "A tool" in r.content
def test_features(): r = generate("P", features=["Fast", "Easy"]); assert "- Fast" in r.content
def test_install(): r = generate("P", install="pip install p"); assert "pip install p" in r.content
def test_usage(): r = generate("P", usage="python main.py"); assert "python main.py" in r.content
def test_license(): r = generate("P", license_type="MIT"); assert "MIT" in r.content
def test_author(): r = generate("P", author="Dev"); assert "Dev" in r.content
def test_sections(): r = generate("P", description="D", features=["F"]); assert len(r.sections) >= 3
def test_word_count(): r = generate("P", description="Hello world"); assert r.word_count > 0
def test_badges(): result = add_badges("# P", [{"label": "build", "url": "http://img", "link": "#"}]); assert "[![build]" in result
def test_no_badges(): result = add_badges("# P", []); assert result == "# P"
def test_toc(): result = add_toc("# P\n\n## Features\n\n## Install\n"); assert "Table of Contents" in result
def test_format(): md = format_result_markdown(generate("P")); assert "README Generator" in md
def test_to_dict(): d = generate("P").to_dict(); assert "sections" in d
