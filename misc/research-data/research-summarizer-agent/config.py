import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
    SEARCH_RESULTS_PER_QUERY = int(os.getenv("SEARCH_RESULTS_PER_QUERY", "3"))
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "5"))
    HISTORY_DIR = os.path.join(os.path.dirname(__file__), "research_history")

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

# Ensure history directory exists
os.makedirs(Config.HISTORY_DIR, exist_ok=True)
