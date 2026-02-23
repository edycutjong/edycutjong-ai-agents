from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import Tool
import json

class SearchTool:
    def __init__(self):
        # backend="api" is often more reliable for structured results
        self.search = DuckDuckGoSearchResults(backend="api")

    def search_gift_links(self, query: str) -> str:
        """
        Searches for gift items and returns a list of results with titles and links.
        """
        try:
            results = self.search.run(query)
            # results is usually a stringified list of dicts or similar format depending on the tool version.
            # We'll try to parse it or just return the raw string.
            return results
        except Exception as e:
            return f"Error searching for {query}: {str(e)}"

    def get_tool(self) -> Tool:
        return Tool(
            name="GiftSearch",
            func=self.search_gift_links,
            description="Useful for finding purchase links for specific items. Input should be a search query."
        )
