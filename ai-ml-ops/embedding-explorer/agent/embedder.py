from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import numpy as np

class Embedder:
    def __init__(self, model_type="openai", model_name=None, api_key=None):
        self.model_type = model_type.lower()
        self.model_name = model_name
        self.api_key = api_key
        self.embedding_model = self._initialize_model()

    def _initialize_model(self):
        if self.model_type == "openai":
            # Prioritize passed api_key, then environment variable
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API Key is required. Please provide it in the UI or set OPENAI_API_KEY environment variable.")
            return OpenAIEmbeddings(
                model=self.model_name or "text-embedding-3-small",
                openai_api_key=api_key
            )
        elif self.model_type == "huggingface":
            # HuggingFace usually doesn't need API key for local models unless gated
            return HuggingFaceEmbeddings(
                model_name=self.model_name or "sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def embed_documents(self, texts):
        """Generates embeddings for a list of texts."""
        if not texts:
            return []
        try:
            embeddings = self.embedding_model.embed_documents(texts)
            return np.array(embeddings)
        except Exception as e:
            raise RuntimeError(f"Error generating embeddings: {e}")

    def embed_query(self, text):
        """Generates embedding for a single query string."""
        if not text:
            return None
        try:
            return np.array(self.embedding_model.embed_query(text))
        except Exception as e:
            raise RuntimeError(f"Error generating query embedding: {e}")
