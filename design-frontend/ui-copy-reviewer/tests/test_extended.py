import pytest
from unittest.mock import patch, MagicMock
from agent.extractor import extract_text_from_file, TextExtractor
from agent.report import ReportGenerator
from agent.reviewer import ReviewerAgent
import config

# extractor.py
def test_extract_text_read_exception(tmp_path):
    path = tmp_path / "test.html"
    path.touch()
    with patch("builtins.open", side_effect=Exception("Read error")):
        res = extract_text_from_file(str(path))
        assert res == []

def test_extract_html_list_attribute(tmp_path):
    path = tmp_path / "test.html"
    with open(path, "w") as f:
        f.write('<div class="a b">Hello</div>')
    ext = TextExtractor()
    ext.copy_attributes.add("class")
    res = ext.extract_text_from_file(str(path))
    assert any(r['text'] == "a b" for r in res)

# report.py
def test_report_empty():
    gen = ReportGenerator([])
    assert "No issues found" in gen.generate_markdown()

def test_report_json():
    gen = ReportGenerator([{"text": "hi"}])
    assert '[\n  {\n    "text": "hi"\n  }\n]' in gen.generate_json() or '[\n  {\n    "text": "hi"\n  }\n]' in gen.generate_json().replace('\r', '')

def test_report_with_line():
    gen = ReportGenerator([{"text": "hi", "line": 10}])
    assert "**Line:** 10" in gen.generate_markdown()

# reviewer.py
def test_reviewer_real_llm(monkeypatch):
    monkeypatch.setattr(config, "USE_MOCK_LLM", False)
    monkeypatch.setattr(config, "OPENAI_API_KEY", "dummy")
    with patch("agent.reviewer.ChatOpenAI") as mock_chat:
        rev = ReviewerAgent()
        assert mock_chat.called

def test_reviewer_exception():
    rev = ReviewerAgent()
    with patch("langchain_core.runnables.base.RunnableSequence.invoke", side_effect=Exception("LLM Error")):
        res = rev.review_text("some text")
        assert "Error during review" in res["Inclusive Language"]

def test_reviewer_items_empty_text():
    rev = ReviewerAgent()
    items = [{"text": ""}, {"text": "hi"}] # second one is len 2, triggers len(text) < 3
    res = rev.review_items(items)
    assert len(res) == 0
