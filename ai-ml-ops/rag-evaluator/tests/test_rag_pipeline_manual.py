import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.rag_pipeline import RAGPipeline
from langchain_core.documents import Document

def test_rag_pipeline_mock():
    print("Initializing RAG Pipeline with mock key...")
    pipeline = RAGPipeline(openai_api_key="sk-mock-key")

    # Replace the embeddings object completely with a Mock
    pipeline.embeddings = MagicMock()
    pipeline.embeddings.embed_documents.return_value = [[0.1] * 1536]
    pipeline.embeddings.embed_query.return_value = [0.1] * 1536

    # Mock Chroma to avoid actual DB operations
    with patch('agent.rag_pipeline.Chroma') as MockChroma:
        # Mock the vectorstore returned by from_documents
        mock_vectorstore = MagicMock()
        MockChroma.from_documents.return_value = mock_vectorstore
        mock_retriever = MagicMock()
        mock_vectorstore.as_retriever.return_value = mock_retriever

        # Test Indexing Logic
        docs = [Document(page_content="Test content")]

        # We need to mock ChatOpenAI as well, as setup_chain instantiates it
        with patch('agent.rag_pipeline.ChatOpenAI') as MockChat:
            pipeline.index_documents(docs)
            print("Index documents called.")

            MockChroma.from_documents.assert_called_once()

            # Mock the chain invocation
            pipeline.chain = MagicMock()
            pipeline.chain.invoke.return_value = "Mock Answer"

            # Test Query Logic
            answer = pipeline.query("Test Question")
            print(f"Query returned: {answer}")
            assert answer == "Mock Answer"

if __name__ == "__main__":
    test_rag_pipeline_mock()
