import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview")

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in .env")
        if not Config.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is missing in .env")
        if not Config.GITHUB_REPO:
            raise ValueError("GITHUB_REPO is missing in .env")
