import os
import sys
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.rag_pipeline import RAGPipeline

@pytest.fixture
def pipeline():
    return RAGPipeline(openai_api_key="sk-mock")

def test_init_no_key():
    with patch("config.Config.OPENAI_API_KEY", None):
        with pytest.raises(ValueError, match="OpenAI API Key is required"):
            RAGPipeline(openai_api_key=None)

def test_index_documents(pipeline):
    pipeline.embeddings = MagicMock()

    with patch("agent.rag_pipeline.Chroma") as MockChroma, \
         patch("agent.rag_pipeline.ChatOpenAI") as MockChat:

        mock_store = MagicMock()
        MockChroma.from_documents.return_value = mock_store

        mock_retriever = MagicMock()
        mock_store.as_retriever.return_value = mock_retriever

        docs = [Document(page_content="test")]
        pipeline.index_documents(docs)

        MockChroma.from_documents.assert_called_once()
        assert pipeline.retriever == mock_retriever
        assert pipeline.chain is not None

def test_query_without_index(pipeline):
    with pytest.raises(ValueError, match="Pipeline not initialized"):
        pipeline.query("question")

def test_retrieve_without_index(pipeline):
    with pytest.raises(ValueError, match="Retriever not initialized"):
        pipeline.retrieve_context("question")

def test_query_mock_chain(pipeline):
    pipeline.chain = MagicMock()
    pipeline.chain.invoke.return_value = "answer"

    assert pipeline.query("question") == "answer"
