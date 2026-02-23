import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200
    DEFAULT_K = 4
    DEFAULT_MODEL = "gpt-3.5-turbo"
    VECTOR_STORE_PATH = "chroma_db"
