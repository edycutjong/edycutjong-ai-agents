import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # If no key is provided, the app can run in demo mode with mocked LLM responses
    DEMO_MODE = os.getenv("DEMO_MODE", "False").lower() in ("true", "1", "t")

    # Path to mock data storage
    DATA_PATH = os.path.join(os.path.dirname(__file__), "mock_data.json")

    # Issue statuses
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_IN_PROGRESS = "in_progress"

    # Teams
    TEAM_BACKEND = "Backend"
    TEAM_FRONTEND = "Frontend"
    TEAM_DEVOPS = "DevOps"
    TEAM_MOBILE = "Mobile"
    TEAM_QA = "QA"

    TEAMS = [TEAM_BACKEND, TEAM_FRONTEND, TEAM_DEVOPS, TEAM_MOBILE, TEAM_QA]
