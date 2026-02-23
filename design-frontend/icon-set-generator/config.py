import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Default settings
    DEFAULT_STYLE = "Line"
    DEFAULT_COLOR = "#000000"
    DEFAULT_SIZE = 24

    # Supported Styles
    STYLES = [
        "Line",
        "Solid",
        "Flat",
        "3D",
        "Hand-drawn",
        "Pixel Art"
    ]

config = Config()
