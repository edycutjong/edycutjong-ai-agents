"""Web search tool — simulated search for the research agent."""

from crewai.tools import tool


@tool("Web Search")
def web_search_tool(query: str) -> str:
    """Search the web for information on a given query.

    This is a placeholder tool that simulates web search results.
    In production, connect to a real search API (SerpAPI, Tavily, etc.).

    Args:
        query: The search query string.

    Returns:
        Simulated search results as a formatted string.
    """
    # In production, replace with actual API calls:
    # - SerpAPI: https://serpapi.com
    # - Tavily: https://tavily.com
    # - Google Custom Search: https://developers.google.com/custom-search
    return (
        f"Search results for: '{query}'\n\n"
        f"Note: This is a simulated search. Connect a real search API "
        f"(SerpAPI, Tavily, or Google Custom Search) for production use.\n\n"
        f"To integrate a real search API:\n"
        f"1. Install the appropriate SDK (e.g., `pip install tavily-python`)\n"
        f"2. Set the API key in .env\n"
        f"3. Replace this function body with actual API calls\n"
    )
