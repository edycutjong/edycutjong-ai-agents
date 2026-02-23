"""Configuration for Agent system — models, execution, and agent settings."""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Model Configuration ────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

LLM_CONFIG = {
    "config_list": [
        {
            "model": MODEL_NAME,
            "api_key": OPENAI_API_KEY,
        }
    ],
    "temperature": 0.1,
    "timeout": 120,
}

# ── Code Execution Configuration ────────────────────────────────────
CODE_EXECUTION_CONFIG = {
    "work_dir": "workspace",
    "use_docker": False,  # Set to True for sandboxed execution
    "timeout": 60,
    "last_n_messages": 3,
}

# ── Agent Personalities ─────────────────────────────────────────────
ASSISTANT_SYSTEM_MESSAGE = """You are a helpful AI assistant that excels at:
1. Writing clean, well-documented Python code
2. Debugging errors systematically
3. Explaining complex concepts clearly
4. Breaking problems into manageable steps

When writing code:
- Always include type hints
- Add docstrings to functions
- Handle edge cases and errors
- Use modern Python features (3.12+)
- Print results clearly for verification

When you encounter an error, analyze it carefully and fix the root cause."""

PLANNER_SYSTEM_MESSAGE = """You are a planning agent that breaks down complex tasks.
Your role is to:
1. Analyze the task requirements
2. Break it into numbered steps
3. Identify potential challenges
4. Suggest a clear execution plan

Do NOT write code yourself — delegate code tasks to the AssistantAgent."""

MAX_CONSECUTIVE_AUTO_REPLY = 10
HUMAN_INPUT_MODE = "NEVER"  # Options: ALWAYS, TERMINATE, NEVER
