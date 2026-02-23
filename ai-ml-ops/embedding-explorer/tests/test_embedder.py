import pytest
from unittest.mock import MagicMock, patch
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.embedder import Embedder

@pytest.fixture
def mock_openai_embeddings():
    with patch("agent.embedder.OpenAIEmbeddings") as mock:
        instance = mock.return_value
        instance.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        instance.embed_query.return_value = [0.1, 0.2, 0.3]
        yield mock

def test_embed_documents(mock_openai_embeddings):
    embedder = Embedder(model_type="openai", api_key="fake-key")
    texts = ["hello", "world"]
    embeddings = embedder.embed_documents(texts)
    assert embeddings.shape == (2, 3)
    assert np.array_equal(embeddings, np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]))

def test_embed_query(mock_openai_embeddings):
    embedder = Embedder(model_type="openai", api_key="fake-key")
    embedding = embedder.embed_query("hello")
    assert embedding.shape == (3,)
    assert np.array_equal(embedding, np.array([0.1, 0.2, 0.3]))
