from unittest.mock import patch, MagicMock
import time
from datetime import datetime
from agent.fetcher import fetch_rss_feed, fetch_article_content

def test_fetch_rss_feed():
    with patch('feedparser.parse') as mock_parse:
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.feed = {'title': 'Test Feed'}

        # Create a mock entry
        entry = MagicMock()
        # Use a real dict for get method to avoid side_effect complexity if possible,
        # or stick to side_effect if attribute access is needed.
        # Feedparser entries are dict-like but also object-like.
        entry.title = "Test Article"
        entry.link = "http://test.com"
        entry.summary = "Test Summary"
        entry.get = lambda k, d=None: getattr(entry, k, d)

        # Set published_parsed to current time
        entry.published_parsed = time.localtime()

        mock_feed.entries = [entry]
        mock_parse.return_value = mock_feed

        articles = fetch_rss_feed("http://feed.url", days=1)
        assert len(articles) == 1
        assert articles[0]['title'] == 'Test Article'
        assert articles[0]['source'] == 'Test Feed'

def test_fetch_rss_feed_old_article():
    with patch('feedparser.parse') as mock_parse:
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.feed = {'title': 'Test Feed'}

        entry = MagicMock()
        entry.title = "Old Article"
        entry.get = lambda k, d=None: getattr(entry, k, d)

        # Set published_parsed to 10 days ago
        old_time = time.time() - (10 * 24 * 3600)
        entry.published_parsed = time.localtime(old_time)

        mock_feed.entries = [entry]
        mock_parse.return_value = mock_feed

        # Fetch with 1 day lookback
        articles = fetch_rss_feed("http://feed.url", days=1)
        assert len(articles) == 0

def test_fetch_article_content():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.content = b'<html><body><h1>Title</h1><p>Test content paragraph.</p></body></html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        content = fetch_article_content("http://test.com")
        assert "Test content paragraph" in content
        assert "Title" in content

def test_fetch_article_content_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection Error")

        content = fetch_article_content("http://test.com")
        assert content == ""

def test_parse_date():
    from agent.fetcher import parse_date

    # Case 1: published_parsed exists
    entry = MagicMock()
    entry.published_parsed = time.localtime()
    assert parse_date(entry) is not None

    # Case 2: updated_parsed exists
    entry = MagicMock()
    del entry.published_parsed
    entry.updated_parsed = time.localtime()
    assert parse_date(entry) is not None

    # Case 3: Neither exists
    entry = MagicMock()
    del entry.published_parsed
    del entry.updated_parsed
    assert parse_date(entry) is None

def test_fetch_rss_feed_exception():
    with patch('feedparser.parse') as mock_parse:
        mock_parse.side_effect = Exception("Feed Error")
        articles = fetch_rss_feed("url")
        assert articles == []
