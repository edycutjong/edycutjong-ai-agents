import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    # Defaults
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        if not cls.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is not set.")

# For local testing, you might want to call validate() manually or when the app starts
