import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4-turbo")
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "meeting_notes.json")

    # UI Theme Settings (can be used in CSS injection)
    THEME_PRIMARY_COLOR = "#FF4B4B"
    THEME_BACKGROUND_COLOR = "#0E1117"
    THEME_TEXT_COLOR = "#FAFAFA"
