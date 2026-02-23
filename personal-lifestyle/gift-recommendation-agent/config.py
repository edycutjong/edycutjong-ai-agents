import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GIFT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "data", "history.json")

    # Defaults
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "duckduckgo")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY and not cls.GEMINI_API_KEY:
            # We don't raise here to allow UI to ask for keys
            pass
