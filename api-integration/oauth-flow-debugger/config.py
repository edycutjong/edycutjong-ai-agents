import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Add other config variables as needed
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
