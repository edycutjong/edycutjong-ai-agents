import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

    # Create directories if they don't exist
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
