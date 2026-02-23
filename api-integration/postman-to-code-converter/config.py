import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "python")
