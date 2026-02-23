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
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append(r['href'])

        return results
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return []

def scrape_website(url: str) -> str:
    """
    Scrape text content from a website using BeautifulSoup.
    """
    try:
        # Use a proper User-Agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        text = soup.get_text(separator=' ', strip=True)

        # Basic cleaning
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text[:10000] # Limit content length
    except Exception as e:
        logger.error(f"Scraping failed for {url}: {e}")
        return ""
