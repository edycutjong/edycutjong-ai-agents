import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4o"
    TEMPERATURE = 0.0

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            # For this sandbox environment, we might not want to fail hard if the key is missing,
            # but in a real app we would. I'll print a warning instead.
            print("Warning: OPENAI_API_KEY is not set. The agent will not function correctly without it.")
            pass
