import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Default settings
    DEFAULT_OUTPUT_DIR = "output"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Cleaning settings
    REMOVE_TAGS = ['nav', 'footer', 'script', 'style', 'iframe', 'noscript', 'header', 'aside']

    def __init__(self):
        pass
