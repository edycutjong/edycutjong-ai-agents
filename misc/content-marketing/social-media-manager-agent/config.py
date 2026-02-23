import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Premium UI Settings
    THEME_COLOR_PRIMARY = "#6366f1"
    THEME_COLOR_SECONDARY = "#8b5cf6"
    THEME_COLOR_ACCENT = "#ec4899"
    THEME_BG_GRADIENT = "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)"

    # App Settings
    APP_NAME = "Nexus Social Manager"
    APP_ICON = "🚀"

    @staticmethod
    def get_api_key():
        return os.getenv("OPENAI_API_KEY")
