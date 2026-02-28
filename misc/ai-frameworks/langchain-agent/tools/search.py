"""Web search tool using DuckDuckGo."""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool


def create_search_tool() -> Tool:
    """Create a DuckDuckGo web search tool.

    Returns:
        Configured search tool for the agent.
    """
    search = DuckDuckGoSearchRun()
    return Tool(
        name="Web Search",
        func=search.run,
        description=(
            "Search the web for current information. "
            "Use this when you need up-to-date facts, news, or data. "
            "Input should be a search query string."
        ),
    )
