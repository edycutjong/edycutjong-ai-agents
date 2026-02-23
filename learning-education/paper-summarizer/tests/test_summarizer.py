import unittest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

class TestPaperSummarizer(unittest.TestCase):

    @patch('agent.summarizer.ChatOpenAI')
    def setUp(self, MockChatOpenAI):
        self.mock_llm_instance = MagicMock()
        self.mock_llm_instance.invoke.return_value = AIMessage(content="Default Content")

        class FakeLLM(Runnable):
            def __init__(self, mock_instance):
                self.mock_instance = mock_instance

            def invoke(self, input, config=None, **kwargs):
                return self.mock_instance.invoke(input, config, **kwargs)

        fake_llm = FakeLLM(self.mock_llm_instance)

        MockChatOpenAI.return_value = fake_llm
        from agent.summarizer import PaperSummarizer
        self.summarizer = PaperSummarizer()
        self.mock_llm = self.mock_llm_instance

    def test_extract_abstract_methodology(self):
        self.mock_llm.invoke.return_value = AIMessage(content="Abstract: ... Methodology: ...")
        result = self.summarizer.extract_abstract_methodology("some text")
        self.assertEqual(result, "Abstract: ... Methodology: ...")

    def test_generate_plain_language_summary(self):
        self.mock_llm.invoke.return_value = AIMessage(content="Simple summary.")
        result = self.summarizer.generate_plain_language_summary("complex text")
        self.assertEqual(result, "Simple summary.")

    def test_extract_key_findings(self):
        self.mock_llm.invoke.return_value = AIMessage(content="- Finding 1")
        result = self.summarizer.extract_key_findings("data")
        self.assertEqual(result, "- Finding 1")

    def test_extract_citations(self):
        self.mock_llm.invoke.return_value = AIMessage(content="[1] Author...")
        result = self.summarizer.extract_citations("references")
        self.assertEqual(result, "[1] Author...")

    def test_summarize_all(self):
        self.mock_llm.invoke.side_effect = [
            AIMessage(content="Abstract/Method"),
            AIMessage(content="Plain Summary"),
            AIMessage(content="Key Findings"),
            AIMessage(content="Citations")
        ]
        result = self.summarizer.summarize_all("text")
        self.assertEqual(result, {
            "abstract_methodology": "Abstract/Method",
            "plain_language_summary": "Plain Summary",
            "key_findings": "Key Findings",
            "citations": "Citations",
        })

if __name__ == '__main__':
    unittest.main()
