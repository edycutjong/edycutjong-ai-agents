import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default database URL for the app
    DEFAULT_DB_URI = "sqlite:///sample_data.db"
    # Agent settings
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0

config = Config()
