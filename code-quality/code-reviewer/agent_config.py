import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        if not Config.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is not set in environment variables.")
