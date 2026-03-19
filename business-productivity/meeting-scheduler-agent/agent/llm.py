import os
from langchain_openai import ChatOpenAI

try:
    from config import OPENAI_API_KEY
except ImportError:  # pragma: no cover
    # If running from inside agent package without proper path setup
    import sys  # pragma: no cover
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pragma: no cover
    from config import OPENAI_API_KEY  # pragma: no cover

def get_llm():
    if not OPENAI_API_KEY:
        # Return a mock or raise error. For agent, usually we need a real LLM.
        # But if we want to run tests without keys, we might want a mock.
        print("Warning: OPENAI_API_KEY not found. Agent cannot be initialized.")
        return None

    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=OPENAI_API_KEY
    )
