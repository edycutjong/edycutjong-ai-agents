"""Configuration for LangChain agent system."""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Agent settings
MAX_ITERATIONS = 10
TEMPERATURE = 0.1
STREAMING = True

# Vector store settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"

# Memory settings
MEMORY_KEY = "chat_history"
MAX_MEMORY_MESSAGES = 20
