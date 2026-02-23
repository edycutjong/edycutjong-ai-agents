import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_TONE = os.getenv("DEFAULT_TONE", "Professional")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")

config = Config()
