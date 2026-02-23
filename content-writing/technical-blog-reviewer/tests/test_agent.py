import pytest
from unittest.mock import MagicMock
from agent.core import TechnicalBlogReviewer

@pytest.fixture
def mock_reviewer(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Mocked LLM Response"

    # Mock ChatOpenAI to return our mock_llm
    mock_cls = MagicMock(return_value=mock_llm)
    monkeypatch.setattr("agent.core.ChatOpenAI", mock_cls)

    return TechnicalBlogReviewer(api_key="sk-fake")

def test_review_accuracy(mock_reviewer):
    content = "Some content"
    response = mock_reviewer._review_accuracy(content)
    assert response == "Mocked LLM Response"

def test_validate_code(mock_reviewer):
    content = "```python\nprint('hello')\n```"
    response = mock_reviewer._validate_code(content)
    assert response == "Mocked LLM Response"

def test_assess_readability(mock_reviewer):
    content = "Some content"
    response = mock_reviewer._assess_readability(content)
    assert response == "Mocked LLM Response"

def test_generate_summary(mock_reviewer):
    content = "Some content"
    response = mock_reviewer._generate_summary(content, "tech", "code", "read")
    assert response == "Mocked LLM Response"

def test_review_full_workflow(mock_reviewer):
    content = "This is a test blog post."
    report = mock_reviewer.review(content)

    assert "technical_accuracy" in report
    assert "code_validation" in report
    assert "readability" in report
    assert "summary" in report
    assert report["technical_accuracy"] == "Mocked LLM Response"

def test_review_url_workflow(mock_reviewer, monkeypatch):
    # Mock extract_text_from_url
    mock_extract = MagicMock(return_value="Extracted Text")
    monkeypatch.setattr("agent.core.extract_text_from_url", mock_extract)

    report = mock_reviewer.review("http://example.com", is_url=True)

    assert report["technical_accuracy"] == "Mocked LLM Response"
    mock_extract.assert_called_once_with("http://example.com")
