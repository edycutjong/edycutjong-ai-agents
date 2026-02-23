import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Agent Settings
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 4096

# Search Settings
SEARCH_MAX_RESULTS = 5
