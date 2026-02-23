import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    # If True, the agent will use mock responses instead of calling LLM APIs.
    # Useful for testing or running without API keys.
    MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() == "true"

    # Path to save/load the learning path data
    DATA_FILE = "learning_path.json"

config = Config()
