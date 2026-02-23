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
        # Patch extract_claims at the instance level to test claim parsing logic
        # We test the regex parsing by directly calling extract_claims with a mocked llm
        # The easiest approach: mock self.detector.llm as a callable that returns
        # an object with .content
        mock_response = MagicMock()
        mock_response.content = "1. Claim one.\n2. Claim two."

        # Create a mock chain that returns mock_response when invoked
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = mock_response

        # Patch the prompt's __or__ to return our mock chain
        with patch('agent.detector.claim_extraction_prompt') as mock_prompt:
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)

            claims = self.detector.extract_claims("Some text")

            self.assertEqual(len(claims), 2)
            self.assertEqual(claims[0], "Claim one.")
            self.assertEqual(claims[1], "Claim two.")

    def test_verify_claim(self):
        # Mock vectorstore search
        mock_doc = MagicMock()
        mock_doc.page_content = "Source text snippet."
        self.mock_vectorstore.similarity_search.return_value = [mock_doc]

        # Mock LLM response for verification
        mock_response = MagicMock()
        mock_response.content = '{"status": "VERIFIED", "confidence": 0.95, "explanation": "Found it."}'

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = mock_response

        with patch('agent.detector.verification_prompt') as mock_prompt:
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)

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
