import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:  # pragma: no cover
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")  # pragma: no cover
        if not Config.GITHUB_TOKEN:  # pragma: no cover
            raise ValueError("GITHUB_TOKEN is not set in environment variables.")  # pragma: no cover
