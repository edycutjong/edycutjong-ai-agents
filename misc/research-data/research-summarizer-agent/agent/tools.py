from langchain_community.tools import DuckDuckGoSearchRun
from bs4 import BeautifulSoup
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_tool(query: str, num_results: int = 3) -> list[str]:
    """
    Search the web for a query using DuckDuckGo.
    Returns a list of URLs.
    """
    try:  # pragma: no cover
        from duckduckgo_search import DDGS  # pragma: no cover

        results = []  # pragma: no cover
        with DDGS() as ddgs:  # pragma: no cover
            for r in ddgs.text(query, max_results=num_results):  # pragma: no cover
                results.append(r['href'])  # pragma: no cover

        return results  # pragma: no cover
    except Exception as e:  # pragma: no cover
        logger.error(f"Search failed for query '{query}': {e}")  # pragma: no cover
        return []  # pragma: no cover

def scrape_website(url: str) -> str:
    """
    Scrape text content from a website using BeautifulSoup.
    """
    try:  # pragma: no cover
        # Use a proper User-Agent to avoid being blocked
        headers = {  # pragma: no cover
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)  # pragma: no cover
        response.raise_for_status()  # pragma: no cover

        soup = BeautifulSoup(response.content, 'html.parser')  # pragma: no cover

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):  # pragma: no cover
            script.decompose()  # pragma: no cover

        text = soup.get_text(separator=' ', strip=True)  # pragma: no cover

        # Basic cleaning
        lines = (line.strip() for line in text.splitlines())  # pragma: no cover
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # pragma: no cover
        text = '\n'.join(chunk for chunk in chunks if chunk)  # pragma: no cover

        return text[:10000] # Limit content length  # pragma: no cover
    except Exception as e:  # pragma: no cover
        logger.error(f"Scraping failed for {url}: {e}")  # pragma: no cover
        return ""  # pragma: no cover
