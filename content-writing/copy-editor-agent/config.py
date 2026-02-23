import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4o"
    TEMPERATURE = 0.7

    # Style Guide Defaults
    DEFAULT_STYLE_GUIDE = "AP Style"
    DEFAULT_TONE = "Professional"

    # Readability Thresholds (Example)
    READABILITY_TARGET = 60  # Flesch Reading Ease score target (60-70 is standard)
    MAX_PASSIVE_VOICE_PERCENTAGE = 10  # Flag if > 10% sentences are passive
