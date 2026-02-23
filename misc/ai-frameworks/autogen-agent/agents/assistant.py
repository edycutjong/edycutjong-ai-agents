"""AssistantAgent configuration — the AI that writes and debugs code."""

from autogen import AssistantAgent
from config import LLM_CONFIG, ASSISTANT_SYSTEM_MESSAGE


def create_assistant(name: str = "assistant") -> AssistantAgent:
    """Create an AssistantAgent that plans and writes code.

    Args:
        name: The agent's name in conversations.

    Returns:
        Configured AssistantAgent instance.
    """
    return AssistantAgent(
        name=name,
        system_message=ASSISTANT_SYSTEM_MESSAGE,
        llm_config=LLM_CONFIG,
        code_execution_config=False,  # Assistant doesn't execute code itself
    )


def create_planner(name: str = "planner") -> AssistantAgent:
    """Create a planner agent for task decomposition.

    Args:
        name: The agent's name in conversations.

    Returns:
        Configured planner AssistantAgent instance.
    """
    from config import PLANNER_SYSTEM_MESSAGE

    return AssistantAgent(
        name=name,
        system_message=PLANNER_SYSTEM_MESSAGE,
        llm_config=LLM_CONFIG,
        code_execution_config=False,
    )
