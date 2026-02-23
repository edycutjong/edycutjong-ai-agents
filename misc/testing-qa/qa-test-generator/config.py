import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default model
    MODEL_NAME = "gpt-4-turbo"
    # Testing configuration
    TEST_TIMEOUT = 30000  # ms
    HEADLESS = True

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    GENERATED_TESTS_DIR = os.path.join(BASE_DIR, "generated_tests")

    @staticmethod
    def ensure_dirs():
        if not os.path.exists(Config.GENERATED_TESTS_DIR):
            os.makedirs(Config.GENERATED_TESTS_DIR)

# Initialize
Config.ensure_dirs()
