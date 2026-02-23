import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "okrs.json")
