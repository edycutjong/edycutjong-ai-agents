import os
from dotenv import load_dotenv

load_dotenv()

# Fallback to JULES_API_KEY if OPENAI_API_KEY is not set
if not os.getenv("OPENAI_API_KEY") and os.getenv("JULES_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("JULES_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

if not OPENAI_API_KEY:
    # We might not fail immediately to allow tests to run without keys if mocked
    pass
