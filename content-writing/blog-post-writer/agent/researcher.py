from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List

from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
from prompts.research_prompts import RESEARCH_SUMMARY_PROMPT

class Researcher:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        self.search_tool = DuckDuckGoSearchRun()
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
        self.summary_chain = RESEARCH_SUMMARY_PROMPT | self.llm

    def research(self, topic: str) -> Dict[str, Any]:
        """Performs research on the given topic."""
        print(f"Researching topic: {topic}...")

        # Perform search
        try:
            search_results = self.search_tool.run(topic)
        except Exception as e:
            print(f"Error during search: {e}")
            search_results = "Search failed. Proceeding with limited information."

        print(f"Search results obtained. Summarizing...")

        # Summarize results
        summary_response = self.summary_chain.invoke({
            "topic": topic,
            "search_results": search_results
        })

        summary = summary_response.content if hasattr(summary_response, 'content') else str(summary_response)

        return {
            "topic": topic,
            "raw_search_results": search_results,
            "summary": summary
        }

if __name__ == "__main__":
    # Test the researcher
    researcher = Researcher()
    result = researcher.research("AI in content marketing")
    print(result['summary'])
