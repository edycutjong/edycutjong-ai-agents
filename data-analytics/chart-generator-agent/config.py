import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

    @classmethod
    def check_api_keys(cls):
        if not cls.OPENAI_API_KEY and not cls.GOOGLE_API_KEY:
            raise ValueError("No API key found. Please set OPENAI_API_KEY or GOOGLE_API_KEY in .env file.")
