import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
