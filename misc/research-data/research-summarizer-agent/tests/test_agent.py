import unittest
from unittest.mock import MagicMock, patch, ANY
from agent.researcher import ResearchAgent
from langchain_core.messages import AIMessage

class TestResearchAgent(unittest.TestCase):

    @patch('agent.researcher.ChatOpenAI')
    @patch('agent.researcher.search_tool')
    @patch('agent.researcher.scrape_website')
    def test_run_research(self, mock_scrape, mock_search, mock_chat_openai):
        # Setup mock LLM instance
        mock_llm = MagicMock()
        mock_chat_openai.return_value = mock_llm

        # Define side effects for LLM calls
        # 1. Plan: "1. Step One"
        # 2. Queries: "query1\nquery2"
        # 3. Synthesis: "Synthesized text"
        # 4. Fact Check: "Checked text"
        # 5. Final Report: "# Final Report Content"

        side_effects = [
            AIMessage(content="1. Step One"), # plan_research
            AIMessage(content="query1"),      # generate_search_queries
            AIMessage(content="Synthesized text about Step One"), # synthesize_info
            AIMessage(content="Fact Checked Step One"),     # fact_check
            AIMessage(content="# Final Report\n\nChecked Step One"), # generate_final_report
        ]

        mock_llm.invoke.side_effect = side_effects
        mock_llm.return_value = side_effects[0] # Just in case
        # Also mock __call__ just in case LangChain calls it directly
        mock_llm.side_effect = side_effects

        # Mock tools
        mock_search.return_value = ["http://example.com"]
        mock_scrape.return_value = "Scraped content from example.com"

        # Initialize agent
        agent = ResearchAgent()

        # Run research
        final_report = agent.run_research("Test Topic", "Overview", ["Technology"])

        # Assertions
        self.assertIn("Final Report", final_report)
        # Check if called either via invoke or __call__
        total_calls = mock_llm.invoke.call_count + mock_llm.call_count
        self.assertEqual(total_calls, 5)

        # Verify tools called
        mock_search.assert_called_with("query1", num_results=ANY)
        mock_scrape.assert_called_with("http://example.com")

if __name__ == '__main__':
    unittest.main()
