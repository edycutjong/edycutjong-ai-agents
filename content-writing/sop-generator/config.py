import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

    @staticmethod
    def setup_logging():
        logging.basicConfig(
            level=Config.LOG_LEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler()
            ]
        )

# Initialize logging
Config.setup_logging()
logger = logging.getLogger(__name__)
