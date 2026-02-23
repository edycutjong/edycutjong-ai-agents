import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.detector import HallucinationDetector

class TestHallucinationDetector(unittest.TestCase):

    @patch('agent.detector.ChatOpenAI')
    @patch('agent.detector.OpenAIEmbeddings')
    @patch('agent.detector.FAISS')
    def setUp(self, MockFAISS, MockOpenAIEmbeddings, MockChatOpenAI):
        self.mock_llm = MockChatOpenAI.return_value
        self.mock_embeddings = MockOpenAIEmbeddings.return_value
        self.mock_vectorstore = MockFAISS.return_value

        # Mock FAISS from_documents
        MockFAISS.from_documents.return_value = self.mock_vectorstore

        self.detector = HallucinationDetector(api_key="test-key")

    def test_extract_claims(self):
        # Mock LLM response
        self.mock_llm.predict.return_value = "1. Claim one.\n2. Claim two."
        # Or if using LLMChain.run (which calls llm)
        # We need to mock LLMChain behavior or the llm call inside it.
        # Since extract_claims uses LLMChain, let's mock LLMChain.run

        with patch('agent.detector.LLMChain') as MockLLMChain:
            mock_chain = MockLLMChain.return_value
            mock_chain.run.return_value = "1. Claim one.\n2. Claim two."

            claims = self.detector.extract_claims("Some text")

            self.assertEqual(len(claims), 2)
            self.assertEqual(claims[0], "Claim one.")
            self.assertEqual(claims[1], "Claim two.")

    def test_verify_claim(self):
        # Mock vectorstore search
        mock_doc = MagicMock()
        mock_doc.page_content = "Source text snippet."
        self.mock_vectorstore.similarity_search.return_value = [mock_doc]

        # Mock LLM verification result
        mock_json_response = '{"status": "VERIFIED", "confidence": 0.95, "explanation": "Found it."}'

        with patch('agent.detector.LLMChain') as MockLLMChain:
            mock_chain = MockLLMChain.return_value
            mock_chain.run.return_value = mock_json_response

            result = self.detector.verify_claim("Claim one.", self.mock_vectorstore)

            self.assertEqual(result["status"], "VERIFIED")
            self.assertEqual(result["confidence"], 0.95)
            self.assertEqual(result["explanation"], "Found it.")
            self.assertEqual(len(result["sources"]), 1)

    @patch('agent.detector.load_document')
    @patch('agent.detector.split_documents')
    def test_process(self, mock_split, mock_load):
        # Setup mocks
        mock_load.return_value = ["raw doc"]
        mock_split.return_value = ["chunk1", "chunk2"]

        # Mock extract_claims and verify_claim methods on the instance
        self.detector.extract_claims = MagicMock(return_value=["Claim 1"])
        self.detector.verify_claim = MagicMock(return_value={
            "status": "VERIFIED", "confidence": 1.0, "explanation": "ok", "sources": []
        })

        # Mock process_document to return the mocked vectorstore
        self.detector.process_document = MagicMock(return_value=self.mock_vectorstore)

        result = self.detector.process("AI Text", "path/to/source.pdf")

        self.assertEqual(result["score"], 100.0)
        self.assertEqual(len(result["results"]), 1)
        self.detector.process_document.assert_called_with("path/to/source.pdf")

if __name__ == '__main__':
    unittest.main()
