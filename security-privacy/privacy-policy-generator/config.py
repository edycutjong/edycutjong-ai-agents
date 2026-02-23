import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Defaults
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

    @classmethod
    def validate(cls):
        """Check for critical configuration"""
        # We can run without API keys if we are just scanning,
        # but generation will fail.
        pass
