import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default model parameters
    DEFAULT_EMBEDDING_MODEL = "openai"  # or "huggingface"
    DEFAULT_REDUCTION_METHOD = "tsne"   # or "pca", "umap"
    DEFAULT_CLUSTERS = 5
    DEFAULT_PERPLEXITY = 30
    DEFAULT_LEARNING_RATE = 200

    # Path configuration
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
