import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Default settings
    DEFAULT_MODEL_PROVIDER = "openai"  # or "google"
    DEFAULT_OPENAI_MODEL = "gpt-4-turbo"
    DEFAULT_GOOGLE_MODEL = "gemini-1.5-pro"

    # UI Theme settings
    THEME_PRIMARY_COLOR = "#FF4B4B"
    THEME_BACKGROUND_COLOR = "#0E1117"
    THEME_TEXT_COLOR = "#FAFAFA"
