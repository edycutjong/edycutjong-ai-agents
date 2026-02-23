import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Default provider: 'openai' or 'google'
    DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

    # Model names
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    # Using gemini-1.5-flash as it is multimodal and efficient
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

    # Batch size for processing images
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5"))

    # Output format
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")

    @classmethod
    def validate(cls):
        if cls.DEFAULT_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        if cls.DEFAULT_PROVIDER == "google" and not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set.")

config = Config()
