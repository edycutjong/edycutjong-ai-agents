import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import mktime
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_date(entry) -> Optional[datetime]:
    """Parse date from feed entry."""
    if hasattr(entry, 'published_parsed'):
        return datetime.fromtimestamp(mktime(entry.published_parsed))
    elif hasattr(entry, 'updated_parsed'):
        return datetime.fromtimestamp(mktime(entry.updated_parsed))
    return None

def fetch_rss_feed(url: str, days: int = 7) -> List[Dict]:
    """
    Fetch and parse an RSS feed, returning a list of articles from the last N days.

    Args:
        url (str): The RSS feed URL.
        days (int): Number of days to look back.

    Returns:
        List[Dict]: A list of dictionaries containing article metadata.
    """
    try:
        logger.info(f"Fetching RSS feed: {url}")
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.warning(f"Feed parser reported error for {url}: {feed.bozo_exception}")

        articles = []
        cutoff_date = datetime.now() - timedelta(days=days)

        for entry in feed.entries:
            published_date = parse_date(entry)

            # If no date found, we might accept it or skip. Let's accept for now but log.
            if not published_date:
                logger.debug(f"No date found for article: {entry.get('title', 'Unknown')}")
                # Optional: Skip if strict date filtering is needed
                # continue
                published_date = datetime.now() # Fallback? Or just don't filter.

            if published_date >= cutoff_date:
                articles.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": published_date,
                    "summary": entry.get("summary", ""),
                    "source": feed.feed.get("title", "Unknown Source")
                })

        logger.info(f"Found {len(articles)} articles from {url} in the last {days} days.")
        return articles

    except Exception as e:
        logger.error(f"Error fetching RSS feed {url}: {str(e)}")
        return []

def fetch_article_content(url: str) -> str:
    """
    Fetch the main content of an article from its URL.

    Args:
        url (str): The article URL.

    Returns:
        str: The text content of the article.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Limit content length to avoid token limits (rudimentary)
        return text[:10000]

    except Exception as e:
        logger.error(f"Error fetching article content from {url}: {str(e)}")
        return ""
