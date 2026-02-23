from unittest.mock import patch, MagicMock
from agent.processor import process_articles

def test_process_articles_success():
    # Mock the dependencies to avoid real API calls
    with patch('agent.processor.get_llm') as mock_get_llm, \
         patch('agent.processor.ANALYSIS_PROMPT') as mock_prompt, \
         patch('agent.processor.JsonOutputParser') as mock_parser_cls:

        # Setup the chain mock
        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        mock_parser = MagicMock()
        mock_parser_cls.return_value = mock_parser

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "relevant": True,
            "summary": "AI is improving.",
            "category": "Artificial Intelligence",
            "score": 9
        }

        # Simulate the LCEL pipe construction: prompt | llm | parser
        # 1. prompt | llm -> runnable1
        mock_runnable1 = MagicMock()
        mock_prompt.__or__.return_value = mock_runnable1

        # 2. runnable1 | parser -> chain
        mock_runnable1.__or__.return_value = mock_chain

        articles = [{"title": "New AI", "link": "http://test.com/ai"}]
        topics = ["AI"]

        processed = process_articles(articles, topics, "fake-api-key")

        assert len(processed) == 1
        assert processed[0]['relevant'] is True
        assert processed[0]['score'] == 9
        assert processed[0]['category'] == "Artificial Intelligence"

def test_process_articles_irrelevant():
    with patch('agent.processor.get_llm') as mock_get_llm, \
         patch('agent.processor.ANALYSIS_PROMPT') as mock_prompt, \
         patch('agent.processor.JsonOutputParser') as mock_parser_cls:

        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "relevant": False,
            "summary": "Boring news.",
            "category": "Other",
            "score": 2
        }

        mock_runnable1 = MagicMock()
        mock_prompt.__or__.return_value = mock_runnable1
        mock_runnable1.__or__.return_value = mock_chain

        articles = [{"title": "Boring News", "link": "http://test.com/boring"}]

        processed = process_articles(articles, ["AI"], "fake-api-key")

        assert len(processed) == 0

def test_process_articles_error():
    with patch('agent.processor.get_llm') as mock_get_llm:
        mock_get_llm.side_effect = Exception("API Error")

        articles = [{"title": "Test", "link": "url"}]
        processed = process_articles(articles, ["AI"], "fake-api-key")

        assert processed == []

def test_process_articles_empty():
    processed = process_articles([], ["AI"], "fake-api-key")
    assert processed == []

def test_process_articles_fetches_content():
    with patch('agent.processor.get_llm') as mock_get_llm, \
         patch('agent.processor.ANALYSIS_PROMPT') as mock_prompt, \
         patch('agent.processor.JsonOutputParser') as mock_parser_cls, \
         patch('agent.processor.fetch_article_content') as mock_fetch:

        mock_llm = MagicMock()
        mock_get_llm.return_value = mock_llm

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {
            "relevant": True,
            "summary": "Summary",
            "category": "Tech",
            "score": 8
        }

        mock_runnable1 = MagicMock()
        mock_prompt.__or__.return_value = mock_runnable1
        mock_runnable1.__or__.return_value = mock_chain

        mock_fetch.return_value = "Fetched Content"

        # Article with short summary -> triggers fetch
        articles = [{"title": "Short", "link": "http://short.com", "summary": "Short summary."}]

        process_articles(articles, ["AI"], "key")

        mock_fetch.assert_called_once_with("http://short.com")

        # Verify chain invoked with fetched content
        # chain.invoke is called with args. Since invoke takes one arg (dict), check call_args.
        args, _ = mock_chain.invoke.call_args
        assert args[0]['content'] == "Fetched Content"

def test_get_llm_google():
    with patch('agent.processor.ChatGoogleGenerativeAI') as MockGoogle:
        from agent.processor import get_llm
        get_llm("key", "google")
        MockGoogle.assert_called_once()

def test_get_llm_invalid():
    from agent.processor import get_llm
    import pytest
    with pytest.raises(ValueError):
        get_llm("key", "invalid")
