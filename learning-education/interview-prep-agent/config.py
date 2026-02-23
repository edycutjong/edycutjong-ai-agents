import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # In a real app we might raise an error, but for now we'll just warn
    # or rely on the user to set it if they want real LLM calls.
    pass

MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.7
