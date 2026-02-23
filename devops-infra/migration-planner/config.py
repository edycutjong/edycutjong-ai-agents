import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Default to Gemini if no API key is set for OpenAI, but prefer Gemini if set
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini" if GEMINI_API_KEY else "openai")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro" if LLM_PROVIDER == "gemini" else "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

config = Config()
