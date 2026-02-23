import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    DEFAULT_INDENT = int(os.getenv("DEFAULT_INDENT", "2"))
