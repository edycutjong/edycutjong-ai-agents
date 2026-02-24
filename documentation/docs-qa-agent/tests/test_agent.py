import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_ask_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"answer": "Use the login() function", "sources": ["auth.md"], "confidence": 0.9, "follow_up_questions": ["How to configure OAuth?"], "tasks": []}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import DocsQAAgent
    agent = DocsQAAgent()
    result = agent.ask("# Auth\nUse login() to authenticate.", "How do I log in?")

    assert isinstance(result, dict)
    assert "login" in result["answer"].lower()
    assert result["confidence"] == 0.9
    mock_model.generate_content.assert_called_once()


def test_ingest_docs_file(tmp_path):
    doc = tmp_path / "readme.md"
    doc.write_text("# Hello\nWorld")

    from src.agent import DocsQAAgent
    agent = DocsQAAgent.__new__(DocsQAAgent)
    content = agent.ingest_docs(str(doc))
    assert "Hello" in content
    assert "World" in content


def test_ingest_docs_directory(tmp_path):
    (tmp_path / "a.md").write_text("# File A")
    (tmp_path / "b.txt").write_text("File B content")
    (tmp_path / "c.py").write_text("# ignored")

    from src.agent import DocsQAAgent
    agent = DocsQAAgent.__new__(DocsQAAgent)
    content = agent.ingest_docs(str(tmp_path))
    assert "File A" in content
    assert "File B" in content
    assert "ignored" not in content
