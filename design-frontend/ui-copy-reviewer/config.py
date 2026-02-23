import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default to fake LLM if no keys are provided, useful for testing/demo
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "False").lower() == "true"
