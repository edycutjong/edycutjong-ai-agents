import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Add other configuration variables as needed
    DATASET_OUTPUT_DIR = os.getenv("DATASET_OUTPUT_DIR", "output_datasets")

    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
